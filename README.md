# Twisted Mixed Multilayer Graphene -- a tunable model

A widget for the calculation and visualization of twisted multilayer graphene systems powered by Dash.

To run this via Docker, do:
1. Clone this repository
2. Run `docker build -t tgkp-docker-dev .`
3. Run `docker run --rm -it -p 5000:5000 tgkp-docker-dev`
4. Go to http://0.0.0.0:5000/

The Fortran code is included in /src/fortran/ and was taken from [twisted_graphene_system_kp_model](https://github.com/quanshengwu/wannier_tools/tree/master/utility/twisted_graphene_system_kp_model). See this repository for instructions on how to compile the code.

If you find any bugs or have any questions, please reach out to leo.goutte@mail.mcgill.ca

Written by Leo Goutte and QuanSheng Wu (EPFL, MARVEL)