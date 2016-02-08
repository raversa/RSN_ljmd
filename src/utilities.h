/* helper function: apply minimum image convention */
double pbc(double x, const double boxby2);

/* helper function: zero out an array */
void azzero(double *d, const int n);

/* compute kinetic energy */
void ekin(mdsys_t *sys);
