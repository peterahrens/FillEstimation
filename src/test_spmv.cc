#include <float.h>
#include <stdio.h>
#include <stdlib.h>
#include <taco.h>
#include <chrono>

using namespace taco;

int test (int m,
          int n,
          int nnz,
          const int *ptr,
          const int *ind,
          const double *data,
          int r,
          int c,
          int trials,
          int verbose,
          double *time_total,
          double *time_mean){

  Format  csr({Dense,Sparse});
  Format bcsr({Dense,Sparse,Dense,Dense});
  Format  bdv({Dense,Dense});
  Format   dv({Dense});

  int bm = (m + r - 1)/r;
  int bn = (n + c - 1)/c;
  int mm = bm * r;
  int nn = bn * c;

  // Create tensors
  Tensor<double> A({bm, bn, r, c}, bcsr);
  Tensor<double> b({bm, r},   bdv);
  Tensor<double> x({bn, c},   bdv);

  Tensor<double> Ap({m, n}, csr);
  Tensor<double> bp({m}, dv);
  Tensor<double> xp({n}, dv);

  {
    int i = 0;
    for (int h = 0; h < nnz; h++){
      while (ptr[i + 1] <= h) {
        i++;
      }
      int j = ind[h];
      A.insert({i/r, j/c, i%r, j%c}, data[h]);
    }
  }

  {
    int i = 0;
    for (int h = 0; h < nnz; h++){
      while (ptr[i + 1] <= h) {
        i++;
      }
      int j = ind[h];
      Ap.insert({i, j}, data[h]);
    }
  }

  for(int h = 0; h < nn; h++){
    x.insert({h/c, h%c}, 1.0);
  }

  for(int h = 0; h < n; h++){
    xp.insert({h}, 1.0);
  }

  A.pack();
  Ap.pack();

  x.pack();
  xp.pack();

  // Form a matrix-vector multiplication expression
  IndexVar i, j, k, l;
  b(i, k) = A(i, j, k, l) * x(j,l);
  bp(i) = Ap(i, j) * xp(j);

  // Compile the expression
  b.compile();
  b.assemble();
  bp.compile();
  bp.assemble();

  double time;

  if (r == 1 && c == 1) {
    //Load problem into cache
    bp.compute();

    //Benchmark some runs
    auto tic = std::chrono::high_resolution_clock::now();
    for (int t = 0; t < trials; t++){
      bp.compute();
    }
    auto toc = std::chrono::high_resolution_clock::now();
    auto diff = std::chrono::duration_cast<std::chrono::nanoseconds>(toc-tic);
    time = diff.count() * 1e-9;
  } else {
    //Load problem into cache
    b.compute();

    //Benchmark some runs
    auto tic = std::chrono::high_resolution_clock::now();
    for (int t = 0; t < trials; t++){
      b.compute();
    }
    auto toc = std::chrono::high_resolution_clock::now();
    auto diff = std::chrono::duration_cast<std::chrono::nanoseconds>(toc-tic);
    time = diff.count() * 1e-9;
  }

  *time_total = time;
  *time_mean = time/trials;
  return 0;
}
