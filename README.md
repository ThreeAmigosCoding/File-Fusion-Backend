# File Fusion

## Overview
The project is a web application for storing and managing photos and videos, similar to the gallery function on mobile devices. The application uses AWS cloud services and follows a serverless architecture.

## User Types
- ### Unauthenticated user 
    Can register to the system. If they already have an account, they can log in to the system.
- ### Authenticated user 
    A user who has successfully logged into the system. They can upload new content to the system and modify or delete existing content. They can manage their photo albums, grant access to their content to another user, revoke granted access, and download the uploaded content locally.

## System Parts
- ### [Client application](https://github.com/ThreeAmigosCoding/File-Fusion-Frontend)
    Provides a graphical interface through which users access the system's functionalities.
- ### [Server application](https://github.com/ThreeAmigosCoding/File-Fusion-Backend)
    A serverless application that contains the entire business logic of the system.

## Functional Requirements
- ### User Registration
    Users can register themselves by providing personal details including name, surname, address, email, and password.
- ### System Login
    Users are able to log into the system using their email and password.
- ### Content Upload
    Users can upload various types of content along with additional information.
- ### Content Access
    Users can view their own content.
- ### Content Modification
    Users can alter content they own.
- ### Content Deletion
    Users are able to delete their own content.
- ### Album Creation
    Users can create new albums and move or add content to them.
- ### Album Deletion
    Users can delete albums (excluding the initial one).
- ### Content Sharing
    Users can share individual pieces of content or entire albums with other users, granting read-only access.
- ### Revoking Content Sharing
    Users can revoke access rights they previously granted to shared content.
- ### Content Download
    Users can download content they have access to, whether they own it or have been granted shared access.
- ### Family Member Registration Process
    The system facilitates a family member registration process using appropriate AWS services.

## Non-Functional Requirements
- ### Serverless Architecture
    The system utilizes a serverless architecture model, leveraging appropriate AWS services.
- ### Separate Storage
    The system separately stores content and associated additional information.
- ### Infrastructure as Code
    The system employs Infrastructure as Code tools for instantiation and configuration of required services.
- ### Asynchronous Communication
    The system enables asynchronous communication between its components, as necessary.
- ### API Gateway
    The system includes an API gateway, which offers a REST API for client-server communication.
- ### Notification System
    The system sends notifications to users when content is successfully stored, modified, or deleted.
- ### Consistency Issue Resolution
    The system tackles potential inconsistencies arising from storing content and additional information separately.

## Authors
- [Miloš Čuturić](https://github.com/cuturic01)
- [Luka Đorđević](https://github.com/lukaDjordjevic01)
- [Marko Janošević](https://github.com/janosevicsm)

## Academic Context
This project was developed for the purposes of the course [Cloud Computing](http://www.ftn.uns.ac.rs/336274786/racunarstvo-u-oblaku).
### Course Assistant
- Eva Janković
### Course Professor
- Miroslav Zarić

![Background](https://github.com/ThreeAmigosCoding/File-Fusion-Frontend/blob/master/src/assets/images/Logo.png)
