
<h2 align="center">QUADROTOR FIS</h2>

<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
<br>
[![MIT License][license-shield]][license-url]
[![Build][build-shield]][license-url]
<br>
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

---

<p align="center"> Few lines describing your project.
    <br> 
</p>

## Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Deployment](#deployment)
- [Usage](#usage)
- [Built Using](#built_using)
- [Authors](#authors)

## About <a name = "about"></a>

This research is a new planning of local route planning based on fuzzy logic capable of maneuvering an air vehicle over an unknown environment, a world of diverse obstacles.

## Getting Started <a name = "getting_started"></a>

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See [deployment](#deployment) for notes on how to deploy the project on a live system.


### Prerequisites

```
mkdir -p quadrotor-ws/src
cd quadrotor-ws/src
git clone --recursive https://github.com/marcelo-leite/autonomy-quadrotor-mfis.git
```

```
cd ..
rosdep install --from-paths src --ignore-src -r -y
catkin_make
source devel/setup.bash
```


## Usage <a name="usage"></a>


Launch simulation with rviz e a user interface window of Gazebo:
```
roslaunch hector_quadrotor_demo obstacles_world.lauch gui:=true
```

Launch simulation with rviz without a user interface window of Gazebo: 
```
roslaunch  hector_quadrotor_demo obstacles_world.lauch gui:=false
```
## Built Using <a name = "built_using"></a>

- [ROS](https://www.ros.org/) - Robot Operating System


## Author <a name = "authors"></a>

- [@Marcelo Leite](https://github.com/leite-marcelo) - Student Electrical Engineer
- [@Selmo Eduardo](https://github.com/selmoeduardo) - Dr. Electrical Engineer

## Sponsors

This research is funded thanks to the generous support of

<div  align="center">
    <img src="https://www.fapema.br/wp-content/uploads/2022/05/logo-FAPEMA-AZUL-top1.png"alt="drawing" height="150"/>
    <img src="https://estudenoifma.ifma.edu.br/wp-content/themes/ps-theme-master/img/footer-marca.png" alt="drawing" height="90"/>

</div>







<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/marcelo-leite/autonomy-quadrotor-mfis.svg?style=for-the-badge
[contributors-url]: https://github.com/marcelo-leite/autonomy-quadrotor-mfis/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/marcelo-leite/autonomy-quadrotor-mfis.svg?style=for-the-badge
[forks-url]: https://github.com/marcelo-leite/autonomy-quadrotor-mfis/network/members
[stars-shield]: https://img.shields.io/github/stars/marcelo-leite/autonomy-quadrotor-mfis.svg?style=for-the-badge
[stars-url]: https://github.com/marcelo-leite/autonomy-quadrotor-mfis/stargazers
[issues-shield]: https://img.shields.io/github/issues/marcelo-leite/autonomy-quadrotor-mfis.svg?style=for-the-badge
[issues-url]: https://github.com/marcelo-leite/autonomy-quadrotor-mfis/issues
[license-shield]: https://img.shields.io/github/license/marcelo-leite/autonomy-quadrotor-mfis.svg?style=for-the-badge
[license-url]: https://github.com/marcelo-leite/autonomy-quadrotor-mfis/LICENSE.txt

[build-shield]: https://img.shields.io/docker/automated/marcelo-leite/autonomy-quadrotor-mfis?style=for-the-badge

[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/leite-marcelo



