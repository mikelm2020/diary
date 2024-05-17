<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/mikelm2020/diary">
    <img src="https://github.com/mikelm2020/diary/blob/961be498851fc7b1e9d940550e7eb54ea3b2130f/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">diary</h3>

  <p align="center">
    An backend for a diary similar to Android 14
    <br />
    <a href="https://github.com/mikelm2020/diary"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <!-- <a href="https://service-streaming.onrender.com/">View Demo</a> -->
    ·
    <a href="https://github.com/mikelm2020/diary/issues">Report Bug</a>
    ·
    <a href="https://github.com/mikelm2020/diary/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <!-- <li><a href="#roadmap">Roadmap</a></li> -->
    <!-- <li><a href="#contributing">Contributing</a></li> -->
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://github.com/mikelm2020/diary/blob/82a8c694a418723faacf992c5dd76b6e328120f8/api_playlists.png)

This is a personal project of backend for a diary

In this project the objetives are:
* Create a local database with PostgreSQL through Django ORM
* Use JWT with custom user model
* Login with username, email and password
* Verifiy email for activate el user
* Use the package phonenumber_field to validate phones
* Use abstract model in all models
* USe UUID for primary keys in the models
* Create the REST API for CRUD operations through Django Rest Framework
* Use Swagger for document the REST API


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With



* [![Python][Python]][Python-url]
* [![Django][Django]][Django-url]
* [![DjangoREST][DjangoREST]][DjangoREST-url]
* [![Swagger][Swagger]][Swagger-url]
* [![JWT][JWT]][JWT-url]
* [![Postgres][Postgres]][Postgres-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

This project use a postgreSQL local database.




### Installation


1. Clone the repository
   ```sh
   git clone https://github.com/mikelm2020/diary.git
   ```
2. Create the python virtual enviroment
3. Prepare the virtual enviroment through of local requirements file in the requirements folder
   ```sh
   pip install -r requirements.txt
   ```
4. Create a .env file with enviroment variables in the root folder

5. The enviroment variables are used in the settings

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

The indications for use the API are:
1. Register an user in the section auth
2. Confirm email in the console
3. Login with the username, email and password in the section auth
4. Copy token refresh of the response
5. Click in authorized button
6. Paste token in value field
7. Click in Authorize button
8. Click in close button
9. Can you use the API
10. Logout in the section auth

<p align="right">(<a href="#readme-top">back to top</a>)</p>


See the [open issues](https://github.com/mikelm2020/diary/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Miguel Angel López Monroy - [@miguellopezmdev](https://twitter.com/miguellopezmdev) - miguel.lopezm.dev@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

My favorite resources used:

* [Choose an Open Source License](https://choosealicense.com)
* [Django Documentation](https://docs.djangoproject.com/en/4.1/)
* [Django Rest Framework Documentation](https://www.django-rest-framework.org/)
* [Django Class Based View Inspector](http://ccbv.co.uk/)
* [Classy Django Rest Framework](https://www.cdrf.co/)
* [Platzi Platform](https://platzi.com/)
* [Udemy Platform](https://www.udemy.com/)
* [Real Python Tutorials](https://realpython.com/)
* [Blog Developer.pe](http://www.developerpe.com/)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/mikelm2020/diary.svg?style=for-the-badge
[contributors-url]: https://github.com/mikelm2020/diary/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mikelm2020/diary.svg?style=for-the-badge
[forks-url]: https://github.com/mikelm2020/diary/network/members
[stars-shield]: https://img.shields.io/github/stars/mikelm2020/diary.svg?style=for-the-badge
[stars-url]: https://github.com/mikelm2020/diary/stargazers
[issues-shield]: https://img.shields.io/github/issues/mikelm2020/diary.svg?style=for-the-badge
[issues-url]: https://github.com/mikelm2020/diary/issues
[license-shield]: https://img.shields.io/github/license/mikelm2020/diary.svg?style=for-the-badge
[license-url]: https://github.com/mikelm2020/diary/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/miguellopezmdev
[product-screenshot]: https://github.com/mikelm2020/diary/blob/82a8c694a418723faacf992c5dd76b6e328120f8/api_playlists.png
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Django]: https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://docs.djangoproject.com/es/4.0/topics/
[DjangoREST]: https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray
[DjangoREST-url]: https://www.django-rest-framework.org/
[Swagger]: https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white
[Swagger-url]: https://swagger.io/
[JWT]: https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens
[JWT-url]: https://jwt.io/
[Postgres]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white
[Postgres-url]: https://www.postgresql.org/

