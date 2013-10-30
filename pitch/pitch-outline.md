Your summary of the Challenge
=============================

*We want your own words here for the Challenge you decide to tackle.*

Your concept of how to address it
================================

*We need enough detail to be able to assess the viability, practicality, supportability, and costs for what you propose.*

Our solution is a web based *workflow engine*, that provides superior flexibility to directorates, a consistent user interface to applicants, and utilises standardised components so it can be constructed within 3 months and maintained cheaply and easily.

Underlying concept
-------------------------

Our concept can be summarised as a flexible, web-based *workflow engine*. 

### Introducing our characters
 * An *applicant* is someone trying to organise an event or apply for a permit.
 * A *directorate* is the body that an applicant must work with to get one or more of the permits they require. Within a directorate, there are 3 roles:
    * An *administrator*, who sets up the application process in terms of workflows, as detailed bleow.
    * An *approver* works with an applicant to progress their application.
    * A *manager* is responsible for balancing the workload amongst approvers.

### What is a workflow?

A workflow is a tailored set of steps to achieve a particular outcome. For example, applying for a permit to serve alcohol is a workflow, and applying for a permit for traffic managment is a workflow.

The concept of a workflow is sufficiently flexible to encompass the range of steps and options in a practical approval process.
 * Workflows can contain steps that an applicant must take, and steps that an approving agency must take. These steps can contain a variety of steps: applicants steps can involve uploading documents, filling in forms, and so on; agency steps can include review, approval, etc.
 * Applicants and agencies can be notified when the application changes from one state to another, for example by email.
 * Workflows do not need to be linear. For example, if an event management plan is insufficient, rather than rejecting the entire application, the applicant can be directed back to resubmitting the event management plan until it is satisfactory.
 TODO IMAGE HERE
 * Workflows can be easily visualised as flow charts, so the status of an application is clear to the applicant and to the approving directorate at a glance.
 * Workflows can contain information about time limits: for example if required documentation is not sumbitted within the required time period, the workflow can automatically transition to an expired state.
 * Workflows can bring together all the relevant documentation in one place. A step that requires an applicant to upload a document can contain information about what the document is supposed to contain. Steps that an approver must take can include information about how a document is to be reviewed, so as to ensure consistency amongst staff. This information is not shown to applicants, so internal processes can be documented.
 * Workflows can contain other workflows: for example a workflow for running an event could guide an applicant through the relevant approvals. Each of those approvals is its own workflow, so if an applicant knows they only need a specific permit, they can do that workflow individually. (This also means that individual directorates can update and improve the workflows for which they are responsible, without it breaking the overall process.)

### Setting up the system

Before an applicant can use the system, an administrator must create workflows.
 * A web interface will allow administrators to build fully functional workflows without requiring additional code to be written. The administrator will be able to specify the steps in the workflow, whether they are done by approvers or the applicant, and provide any information necessary for each step to be completed.
 * The web interface will be able to present the workflow as a flow chart, so that management within the directorate can easily verify that the web process matches up with legislative requirements and existing processes.
 * The workflow will not be presented to the public until it is expressly made live.

### Using the system: applicant

Before an applicant can begin a workflow, they must register as a user. 

Once they register with their name and contact details, they will be presented with a dashboard showing at a glance:
 * **Workflows that they can commence.** Once a workflow is commenced, the directorate is notified, and the application is assigned to an approver.
 * **Any existing applications that they have begun**, and the stage those applications are at. Applicants can pull up the details of their applications and see the entire history in one place. They can then make sure that they have completed any steps necessary for them to complete. The approver responsible for their application is notified whenever the applicant completes a step.
 * **Any completed applications**, should they need to re-download any documents/approvals.


### Using the system: approvers

The workflow system streamlines the job of those tasked with improving applications and makes it easy for them to provide excellent service.

When an approver logs in, they can see at a glance:
 * The applications for which they are responsible.
 * The status of those applications: are they waiting on the applicant, or are they "in my court"?

Approvers can then pull up an application for which they are responsible, see its entire history in one place, and take any steps necessary to progress it. The applicant is notified whenever the approver completes a step.

### Using the system: managers

Managers are responsible for allocating approvers to handle various requests. A manager assigns a workflow that has just commenced to an approver, and is able to re-allocate in-progress workflows if needed. (For example, if an approver is ill or leaves the directorate.)

### Summary of concept

???
 * Flexible
 * Changes do not require programmer intervention
 * Dealing with consistent person, with flexiblity to move if necessary
 * Central repository for information and state: all parties involved can see the progress at a glance, who has to take the next step.


Implementation
--------------------

We intend to implent the system in [Django][django], a well known web framework for the Python programming language. Django is used on sites that deal with millions of hits, so it is known to be able to scale. It is also has a large community of users: if we are hit by a bus, it will be easy to find Django developers to keep the system running.

The implementation will focus on scalability, security and portability.

### Scalibility

The solution has been designed from the ground up for scalability, by decoupling and disaggregating functions into layers that are known to be scalable.

As the diagram shows, TODO DIAGRAM, our solution can be decomposed into a web layer, an application layer, a worker layer and a database layer. 

Each of these layers is horizontally scalable: if heavy usage of the web layer is detected, additional web server can be added without requring any changes to the application code. Similarly, if the database is slow, the database layer can be scaled without requiring the application code to be changed. 

Each layer can be scaled to suit demand, allowing scaling to address the bottleneck without adding unnecessary infrastructure. Similarly, the whole system can be scaled down: the entire system could concievably be run on a single server if demand is not too great.

### Security

Our system is designed to be able to solidly *authenticate* users, determine what those user are *authorised* to do, ensure the *integrity* of their actions and the system as a whole, while maintaining *confidentially* of applicant and directorate information, using industry best practices.

We will deploy SSL at the front end to ensure applicant passwords and information is encrypted while in transit. We will be implementing as much functionality as possible through standard libraries, reducing the scope for security flaws and error on our part. 

We will also be taking a proactive approach to security wherever possible. For example, a major source of security flaws arise from not verifying user input. Our system will make sure that we that user input is valid, make sure that uploaded documents are of the expected format and are free from known viruses, and so on, *before* they are presented to approvers.

### Portability
We will be developing our system on Amazon Web Services (AWS), however our system will not depend on any feature of the AWS infrastructure. This gives the flexibility to either keep the final system on AWS infrastruture, or, if control over data is a concern, to move it to government systems, without requiring chunks of the software to be rewritten. TODO FIX THIS MASSIVE RUN-ON SENTENCE.

We will be ensuring this by using proven, industry-standard, open-source technologies throughout. 

Our current proposed stack is:
 * Our web layer will be implemented with [nginx][nginx].
 * As discussed, our application layer will be implemented with Django.
 * Our worker layer will be implented using [RabbitMQ][rabbitmq]. Having a worker model allows us to perform time-consuming tasks such as scanning for viruses or sending emails without making our user interface non-responsive.
 * Our database layer will be implemented with [PostgreSQL][postgres].
 * Our file storage layer will be implemented using [OpenStack Swift][swift].

If necessary, we may substitute other standard, proven, open-source technologies.

Your proposed project milestones
================================

*As per above, the bake-off projects will run for approximately 3 months.*

The critical dependencies
=========================

*Please tell us what you are assuming, what you will need, to develop your idea into a proper proof-of-concept (POC) with associated case study report.*

Likely costs
============

*To be involved you have to be prepared to give your time voluntarily. So other than your (or your team’s) time, are there any other costs you anticipate incurring in developing your POC. Note that the DCC will fund innovator expenses (based on valid receipts) to a maximum of $5,000.*

Our main cost will be hosting. To ensure we design in a scalable way, we will be using a number of instances on AWS. This prevents us from accidentally making assumptions that will not hold true if the system is scaled up. Our estimate is for 6 AWS t1.micro instances for 3 months, for an estimated $75/month, or $225 for the duration of the bake-off.

We will also have some one-off costs associated with an SSL certificate. This will cost around $75.

Our total estimated costs are $300.

Your full solution assessment
=============================

*Tell us what you think would be involved in turning your concept into a fully working, scalable solution for the challenge.*

The full details for our proof-of-concept are listed above. Assuming our proof-of-concept is successful, the following major steps would be required to deploy it publically.
* Deployment on government servers.
* Training of users within departments.

Your eligibility
================

I, Daniel Axtens, declare:
 * I am a tertiary student at the Australian National University. My university ID is u5376292.
 * There are no conflicts of interest arising if I am involved in implementing the challenge.
