% Digital Canberra Challenge -- Project Design
% DigiACTive Pty Ltd (ABN 62 166 886 871)
% 9 December 2013

# Background #

The ACT Government controls large portions of land within the ACT as public unleased land, including many public parks and nature reserves that are regularly used for events. Holding an event on public unleased land generally requires a permit. Parks and City Services handles approximately 2,500 permit applications per year, covering a wide range of events. Permit applications for large events can be highly complex, involving approval from four or five other government agencies and many pages of supporting documentation.

The current software used for handling land use permits is basic and provides only rudimentary features for managing the permit approval process -- it does not provide an end-to-end system to manage applications from initial submission through to final approval. In particular, all communication with applicants and with other agencies/stakeholders is handled manually via email -- the officer handling the application must manually update the database when an applicant submits an updated document or another agency approves or rejects an application. This process is time-consuming and error-prone.

The process of scoping the project also revealed the following pain points that inform this project:

+ Approvals have to go through multiple agencies, which often fail to respond in a timely manner (if at all). The proliferation of contacts and lines of communication is difficult to manage.
+ It is unclear what permits are needed to organise an event, leading to lots of unnecessary back-and-forth between the department and applicants.
+ Applicants are often unaware how long the process is likely to take, leading to disappointment when permits are not ready in time.
+ Applicants are often unaware of the requirements of the different agencies, leading to lots of lengthy, time consuming and ultimately avoidable dialogs between parties.
+ Applicants are frustrated at how much work has to be done "from scratch" each time they organise an event.

# Objective #

The objective is two-fold:

+ To develop a proof of concept system to demonstrate a workflow-based, online system for use in the assessment and approval of open space for events.
+ To present a case study to the ACT government and NICTA on the experience of the design and development.

# Outcomes #

Initially, the desired outcome of the proof of concept is that TAMS will be able to make a fully informed decision whether or not to engage in a further project to convert the prototype into a full system.

Should TAMS proceed, the desired outcomes of commissioning, developing and deploying a full system are:

+ To increase efficiency of government approval processes, especially multi-agency approvals.
+ To improve the experience of those using the event approval system. In particular, to make it more obvious what is required of applicants and when, what the state of their applications are, and where to go for resources or for help.


# Outputs #

There are two main outputs:

+ A proof of concept system for online assessment and approval of open space for events.
+ A case study documenting DigiACTive and TAMS' experience of the development process.

# Scope of Work/Assumptions and Constraints #

The project has been scoped in the attached scope document, which also documents the assumptions and constraints.

# Governance and Reporting #

Per the project agreement, the project is guided by the Project Board.

The project board consists of:

+ **NICTA**: Michael Phillips
+ **TAMS**: Rachel Reid
+ **DigiACTive**: Benjamin Roberts

Ongoing reporting occurs in the fortnightly project board meeting. The case study is a summative/conclusory report.

# Schedule #

The project has a soft deadline of 26 Feb 2014 (end of last task on the Gantt chart) and a hard deadline of 1 Mar 2014 (expiry of project agreement).

The project is scheduled by the Gantt chart produced by TAMS and stored on the eGovernment Cluster website.

# Budget #

The project budget is $5,000, which is available to DigiACTive for receipted expenses through NICTA.

# Stakeholders & Communication Strategy #

## Collaborative Agreement Parties ##

The Collaborative Agreement defines the interests and communication strategy for **DigiACTive**, **NICTA** and **TAMS**. 


## Community Parties ##

+ **MusicACT**
    + *Stakeholder interest*: MusicACT set the original challenge. Their interest is in the challenge POC being developed into a full system, thereby improving their experience in dealing with government whilst organising their events. They have identified a number of pain points which they would like to see improved. They see this project as part of a broader process of improving government services.
	+ *Communication strategy*: DigiACTive has consulted them in the scoping process and will also work with them in the user testing part of the process.
  
+ **Tuggeranong Community Festival**
    + *Stakeholder interest*: As the organisers of a large event in the territory they have an interest in the event organisation process being streamlined. They have highlighted a need for transparency and visibility regarding an applications processing status. They also identified a need for clarification of the relevant stakeholders requirements when issuing approvals.
    + *Communication strategy*: DigiACTive has consulted them in the scoping process and will also work with them in the user testing part of the process.
    
## Other affected parties ##

+ **SSICT**
    + *Stakeholder interest*: SSICT is responsible for the servers that the project would run on if the POC is converted to a full system. At this stage, none of the code is hosted on SSICT servers.
    + *Communication strategy*: SSICT's requirements are represented by their standards document. The solution is designed to comply with these standards. There is no ongoing communications planned with SSICT at this point.

+ **Other Agencies**:
    + *Stakeholder Interest*: The permit approval process involves several government agencies, including the **Emergency Services Agency**, the **Australian Federal Police**, the **ACT Insurance Authority** and the **Environment Protection Authority**. Each agency is responsible for ensuring that applications meet the relevant requirements within the agency's areas of interest. Each agency has its own policies, procedures and systems for handling applications. 
    + *Communication Strategy*: These agency's interests have been accounted for in the system design. Provision has been made for agencies to communicate effectively with TAMS staff and customers, whether they choose to adopt the system or remain with existing processes and systems (see the Technical Brief for more details). There is no ongoing communications planned with these agencies at this point.


# Risk Management #

At this stage, the output is a proof of concept leading to an outcome of informed decision making.

## Present Risks ##

The risks to the initial outcome are limited:

**Risks:**

+ **Unexpected difficulty of technical component leading to unsatisfactory POC**
    + *Likelihood*: Very likely to occur at various points throughout project.
    + *Severity*: Potentially severe.
    + *Evaluation*: Requires action. See below.

+ **Scope creep/change**
    + This has been effectively mitigated by the signed scope document, and requires no further action.

+ **Conflict in requirements/direction from stakeholders**
    + TAMS/community groups pushing in different directions due to different foci, pain points.
    + Ultimately this will be managed by the Project Board.

+ **DigiACTive team newness/inexperience leading to poor performance**
    + *Likelihood*: Moderate.
    + *Severity*: Potentially severe.
    + *Evaluation*: Managed through the Digital Canberra Challenge/Collaborative Agreement governance structure.

### Management Plan: unexpected technical difficulty ###
It is virtually inevitable in a technical project that some aspect will prove to be unexpectedly difficult.

A number of steps have been taken to reduce the likelihood of this becoming a show-stopping issue:

+ The scope has been managed and restricted. In particular several systems that are unnecessary and difficult/time-consuming for a POC have been put out of the scope.
+ The project has been designed around well known and widely used tools that have proven to be flexible and scalable: we know the tools are up to the task.

We also have a number of strategies to allow us to manage any issues that as they come up:

+ The nature of the POC allows us to "stub out" functionality, to show how it would look and work without actually implementing it. 

    For example, we have decided to "stub out" the payment system by assuming a transaction will succeed without completing further processing. This allows us to integrate payment steps into workflows, without spending our limited time implementing or integrating with a payment system.

+ Our regular meetings allow us to raise unexpected challenges, potentially finding novel ways around these problems that satisfy stakeholders' requirements in a way that is easier to implement.

+ Our links with NICTA, the innovation community in Canberra and with the ANU provide us with networks of experts that can help us resolve issues we may encounter.

Ultimately, this is an unavoidable risk that all software projects bear. We are confident that our mitigation strategies are sufficient.

### Management Plan: DigiACTive team ###
The DigiACTive team is new, and therefore has  the usual risks of new groups and companies.

The risks are largely mitigated by the structure of the Digital Canberra Challenge and the governance arrangements from the Collaborative Agreement.

+ The fortnightly meetings provide the *accountability* necessary to detect problems early.
+ The involvement of NICTA and their experience with early stage commercialisation provides the *resources* and *networks* for DigiACTive to seek help correcting problems as they arise.
+ The structure of the challenge provides a definite end point where the project can be abandoned if it has become unfeasible.

## Avoided Risks/Out of scope risks ##
Risks will need to be reassessed should TAMS wish to proceed to a full system after the proof of concept. However, as it stands, the project poses low risk to TAMS:

+ **The output is a proof of concept that is not publicly accessible.** This closes off a large range of risks:
    + No confidential user data can be lost or stolen as no confidential user data will enter the system.
    + System malfunctions will not lead to embarrassment or public backlash as the system will not be open to the public.
    + System malfunctions will not lead to downtime or lost productivity internally as the system will not be used beyond a small group of testers at this stage.
   
+ TAMS is not committed to take the project further - if it is not fit for purpose or is going to be to expensive, TAMS can decide not to proceed with the project after the project agreement lapses on 1 March. TAMS is not obligated to progress the project beyond that point.
+ The DCC budget is for expense reimbursement only, and is capped at $5000. This is managed by NICTA.


# Related Projects #

The closest related work that DigiACTive is aware of is the existing smart-form system. Apart from that, DigiACTive is unaware of any related projects currently ongoing within PACS.

Looking outside of PACS the other Digital Canberra Challenge project presently running, regarding the booking of drivers' license tests, is tangentially related in that it's a booking system, but targets a different use case and proceeds from a much simpler model - there is no need for multi-agency involvement, for example.

## Future extensions ##

The project scope is explicitly restricted to a proof of concept. Should the project proceed to a full system, there are a couple of related projects:

+ [Plan Your Picnic](http://planyourpicnic.org.au) has been identified as the basis for a possible "front end" to the booking system to allow users to discover the most appropriate land for their use case.
+ More generally, the scoping process identified the desire to build a portal of mostly static information about the available public spaces in the ACT.

# Guidelines & Standards #

While the project is being developed, the project will be built in line with the following guidelines and standards:

+ Industry best practise for security and confidentiality, including the use of:
    + Secure Sockets Layer
	+ Storage of passwords using salts and a password based key derivation function rather than a simple hashing function.
	+ Use of parameterised queries to avoid SQL injection attacks.
	+ Use of proven frameworks over "in house" or DIY technologies.
+ Correct and valid use of technologies such as HTML and CSS, such that all pages pass W3C validation.
+ SSICT standards, such that a full solution can be hosted on SSICT infrastructure with a minimum of intervention.

Before the POC can be deployed, future work will be required to bring it in line with the following other standards:

+ WCAG 2.0 compliance, so as the system meets legislative/human rights requirements for accessibility.
+ ACT Government branding/visual identity

The POC will be developed in such a way as to make that future work as simple as possible.

# Ongoing Quality Control #

Firstly, the outputs are a proof of concept, so an output is "fit for purpose" if it provides a realistic basis on which TAMS can evaluate the feasibility of converting the POC into a full system.

Given the limited duration of the project, there are two major opportunities to verify that the outputs are fit for purpose:

+ In the initial testing of a static workflow.
+ In the final evaluation of the POC for the Digital Canberra Challenge judging process.

In addition, the ongoing reporting provides a regular snapshot of progress and an opportunity to make sure the project stays on track.

There is no formal issue reporting system: emails will suffice. Should the project proceed to a full system, an proper issue/bug tracker will be reconsidered.

# Project Closure and Evaluation #

The initial project has a hard deadline of 1 March 2014, due to the nature of the Digital Canberra Challenge and the terms of the Project Agreement.

Prior to the deadline, DigiACTive will develop a case study documenting its experience.

Following the deadline, the following steps will be taken to close out the project.

+ NICTA evaluates the Proof of Concept and Case Study document for the purposes of deciding a winner in the Digital Canberra Challenge competition.
+ TAMS undertakes an internal evaluation of the proof of concept, leading to a go/no-go decision about undertaking the full system.
+ DigiACTive reassesses its ongoing viability and team in light of TAMS' decision.

# Attachment: Scope Document #

TODO attach in LaTeX

# Attachment: Technical Brief #

This technical brief updates and extends the original pitch outline available on the eGov Cluster shared folder.

The application considers the following "characters":

 * An *applicant* is someone trying to organise an event or apply for a permit.
 * There are one or more *agencies* or *directorates*.

    An *agency* is a body that an applicant must work with to get one or more of the permits they require. In this POC, all applications are initially made to TAMS/PACS, which is an agency.
 
    Within an agency, there are 3 roles:

    * An *administrator*, who sets up the application process in terms of workflows, as detailed below.
    * An *approver* works with an applicant to progress their application.
    * A *manager* is responsible for balancing the workload amongst approvers.

    As part of the application process, an applicant may also deal with other agencies:

    * An applicant may apply directly to the agency for a related permit from within the system.
    * An approver may send part of the application to another agency for feedback/approval.

    Agencies may be either *in the system* or *out of the system*.

    * Agencies that are *in the system* have their own administrators, approvers and managers: they are set up within the DigiApproval system.
    * Agencies that are *out of the system* have approvals sent to them by email. Emails to and from them are stored with the application in a correspondence register.

    This provides a way for the system to interoperate with agencies without them needing to take up the system internally.

## User Interface ##

Based on our pitch, we see the user interface unfolding as follows.

### Applicant

Before an applicant can begin a workflow, they must register as a user. 

Once they register with their name and contact details, they will be presented with a dashboard showing at a glance:

 * **Workflows that they can commence.** Once a workflow is commenced, the directorate is notified, and the application is assigned to an approver.
 * **Any existing applications that they have begun**, and the stage those applications are at. Applicants can pull up the details of their applications and see the entire history in one place. They can then make sure that they have completed any steps necessary for them to complete. The approver responsible for their application is notified whenever the applicant completes a step.
 * **A link to contact the approver assigned to help them progress their workflow**.
 * **A link to access completed applications**, should they need to re-download any documents/approvals, and to help them avoid duplicating effort if they arrange repeated events.

A very loose concept of what this might look like is below:

![User wireframe](./imgs/user-wireframe.png?raw=true)


### Approvers

When an approver logs in, they can see at a glance:

* The applications for which they are responsible.
* The status of those applications:
    * Are they waiting on the applicant?
    * Are they waiting on another agency? Is that agency responding promptly, or have they taken too long?
    * Are they "in my court"?

Approvers can then pull up an application for which they are responsible, see, in one place:

+ The entire history of the application
+ All the communications that have been exchanged
+ How long the application has been pending, both internally, and with any other agencies involved
+ Any steps necessary to progress it.

The applicant is notified whenever the approver completes a step, and approvers (and possibly applicants) are notified when an involved agency provides feedback.

A very loose concept of what this might look like is below. (This concept sketch doesn't include the multi-agency amendments, but that is in scope for the POC.)

![Approver wireframe](./imgs/approver-wireframe.png?raw=true)

### Managers ###

A manager will have a simple user interface to assign a workflow that has just commenced to an approver, and is able to re-allocate in-progress workflows if needed. (For example, if an approver is ill or leaves the directorate.)

Managers will also be able to generate reports, as follows.

### Reporting ###
Based on stakeholder consultation, a reporting front-end has been added, that can generate reports on (at a minimum):

+ A calendar basis: for a day, what permits have been approved?
+ A location basis: for a location, what permits have been approved?
+ A "state" basis: how many approvals are pending? How many have been granted/rejected recently? By whom?

All reports can be generated by managers and administrators. Some reports (calendar/location) can be generated by approvers so as they do not double-book events.

## Technology Stack ##

Our solution can be decomposed into a web layer, an application layer, a set of asynchronous workers and a storage layer (file store and database).

![Application architecture](./imgs/tech-overview.png?raw=true) 

Each of these layers is horizontally scalable.

The system will be implemented in [Django][django]. Django:

+ is a well known web framework for the Python programming language.
+ is used on sites that deal with millions of hits, so it is known to be able to scale.
+ has a large community of users. It will be easy to find Django developers capable of maintaining and extending the system.

The implementation focuses on scalability, security and portability to SSICT systems. It is being built around:

 * **Operating System**: CentOS
     * Largely equivalent to the RHEL environment prescribed by SSICT.
     * Furthermore, our stack should also port without issue to Solaris, as preferred by SSICT.
 * **Provisioning**: [Chef][chef], meeting the SSICT requirement for managed configuration over ad-hoc configuration.
 * **Web server**: [nginx][nginx], deploying SSL throughout.
 * **Application**: Django:
     * Python 3.3 in preference to 2.7.
     * A preference for using existing modules as opposed to developing our own functionality.
     * The workflow engine is [SpiffWorkflow][spiff].
 * **Worker layer**: [RabbitMQ][rabbitmq], interfaced through [Celery][celery].
    * Virus scanning workers will be implemented in [ClamAV][clamav], or possibly stubbed out if we run out of time.
    * Email workers will send mail through Amazon SES, using the SMTP interface for simple transition to SSICT infrastructure.
 * **Database**: [PostgreSQL][postgres].
     * Transition to an Oracle database to meet SSICT requirements should be straightforward thanks to Django's database abstraction. 
 * **File storage**: [OpenStack Swift][swift].
 * **Front end**: [Bootstrap][bootstrap] and [HTML5 boilerplate][h5bp]
     * Developed with an eye towards standards compliance, accessibility and extensibility.

We will be developing our system on Amazon Web Services (AWS), however, all the technologies have been chosen with a view to the code being hosted on SSICT servers should the prototype proceed to a full system.

### Security

Our system is designed to be able to solidly *authenticate* users, determine what those user are *authorised* to do, ensure the *integrity* of their actions and the system as a whole, while maintaining *confidentially* of applicant and directorate information, using industry best practices.

We will deploy SSL at the front end to ensure applicant passwords and information is encrypted while in transit. We will be implementing as much functionality as possible through standard libraries, reducing the scope for security flaws and error on our part. 

We will also be taking a proactive approach to security wherever possible. For example, a major source of security flaws arise from not verifying user input. Our system will make sure that we that user input is valid, make sure that uploaded documents are of the expected format and are free from known viruses, and so on, *before* they are presented to approvers.


[django]: http://django.org "Django"
[nginx]: http://nginx.org/en "nginx"
[rabbitmq]: http://rabbitmq.com "RabbitMQ"
[postgres]: http://postgresql.org "PostgreSQL"
[swift]: http://swift.openstack.org "OpenStack Swift"
[chef]: http://www.opscode.com/chef/ "Chef"
[celery]: http://www.celeryproject.org/ "Celery"
[clamav]: http://www.clamav.net/lang/en/ "Clam AntiVirus"
[spiff]: https://github.com/knipknap/SpiffWorkflow "SpiffWorkflow"
[bootstrap]: http://getbootstrap.com/ "Bootstrap"
[h5bp]: http://html5boilerplate.com/ "HTML5 Boilerplate"
