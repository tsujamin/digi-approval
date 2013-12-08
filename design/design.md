% Digital Canberra Challenge -- Project Design
% DigiACTive Pty Ltd (ABN 62 166 886 871)
% XX December 2013

# Background #

The ACT Government controls large portions of land within the ACT as public unleased land, including many public parks and nature reserves that are regularly used for events. Holding an event on public unleased land generally requires a permit. Parks and City Services handles approximately 2,500 permit applications per year, covering a wide range of events. Permit applications for large events can be highly complex, involving approval from four or five other government agencies and many pages of supporting documentation.

The current software used for handling land use permits is basic and provides only rudimentary features for managing the permit approval process -- it does not provide an end-to-end system to manage applications from initial submission through to final approval. In particular, all communication with applicants and with other agencies/stakeholders is handled manually via email -- the officer handling the application must manually update the database when an applicant submits an updated document or another agency approves or rejects an application. This process is time-consuming and error-prone.

The process of scoping the project also revealed the following pain points that inform this project:

+ Approvals have to go through multiple agencies, which often fail to respond in time. The proliferation of contacts and lines of communication is difficult to manage.
+ It is unclear what permits are needed, leading to lots of unnecessary back-and-forth between the department and applicants.
+ Applicants are often unaware how long the process is likely to take, leading to disappointment when permits are not ready in time.
+ Applicants are often unaware of what the different agencies need, leading to lots of to-ing and fro-ing to sort out the correct details.
+ Applicants are frustrated at how much work has to be done "from scratch" each time.

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

TODO attach

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
    + *Stakeholder interest*: MusicACT set the original challenge. Their interest is in the challenge POC being developed into a full system to improve their experience in dealing with government for the activities they organise. They have identified a number of pain points which they would like to see improved. They see this project as part of a broader process of improving government services.
	+ *Communication strategy*: DigiACTive has consulted them in the scoping process and will also work with them in the user testing part of the process.

## Other affected parties ##

+ **SSICT**
    + *Stakeholder interest*: SSICT is responsible for the servers that the code would run on if the POC is converted to a full system. At this stage, none of the code runs on SSICT servers.
    + *Communication strategy*: SSICT's requirements are represented by their standards document. The solution is designed to comply with these standards. There is no ongoing communications planned with SSICT at this point.

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

+ The scope has been managed and restricted. In particular several systems that are unnecessary for a POC and are fiddly and time consuming have been put out of the scope.
+ The project has been designed around well known and widely used tools that have proven to be flexible and scalable: we know the tools are up to the task.

We also have a number of strategies to allow us to manage any issues that as they come up:

+ The nature of the POC allows us to "stub out" functionality, to show how it would look and work without actually implementing it. 

    For example, we have decided to "stub out" the payment system by making it pretend that all transactions succeed without actually doing anything. This allows us to integrate payment steps into workflows, without spending our limited time implementing or integrating with a payment system.

+ Our regular meetings allow us to raise unexpected challenges, potentially finding novel ways around these problems that satisfy stakeholders' requirements in a way that is easier to implement.

+ Our links with NICTA, the innovation community in Canberra, and with the ANU provide us with networks to find experts to help us resolve any issues we are still stuck with.

Ultimately, this is an unavoidable risk that all software projects bear. We are confident that our mitigation strategies are sufficient.

### Management Plan: DigiACTive team ###
The DigiACTive team is new, and therefore has all the usual risks of new groups and new companies.

The risks are largely mitigated by the structure of the Digital Canberra Challenge and the governance arrangements from the Collaborative Agreement.
+ The fortnightly meetings provide the *accountability* necessary to detect problems early.
+ The involvement of NICTA and their experience with early stage commercialisation provides the *resources* and *networks* for DigiACTive to get help to correct problems as they arise.
+ The structure of the challenge provides a definite end point where the project can be abandoned if it has become unfeasible.

## Avoided Risks/Out of scope risks ##
Risks will need to be reassessed should TAMS wish to proceed to a full system after the proof of concept. However, as it stands, the project poses low risk to TAMS:

+ **The output is a proof of concept that is not publicly accessible.** This closes off a large range of risks:
    + No confidential user data can be lost or stolen as no confidential user data will enter the system.
    + System malfunctions will not lead to embarrassment or public backlash as the system will not be open to the public.
    + System malfunctions will not lead to downtime or lost productivity internally as the system will not be used beyond a small group of testers at this stage.
   
+ TAMS is not committed to take the project further - if it is not fit for purpose or is going to be to expensive, TAMS can decide not to proceed with the project after the project agreement lapses on 1 March. TAMS is not obligated to progress the project beyond that point.
+ The DCC budget is for expense reimbursement only, and is capped at $5000. This money is managed by NICTA.


# Related Projects #

The closest related work that DigiACTive is aware of is the existing smart-form system. Apart from that, DigiACTive is unaware of any related projects currently ongoing within PACS.

Looking outside of PACS, the other Digital Canberra Challenge project, for the booking of drivers' license tests, is tangentially related in that it's a booking system, but proceeds from a much simpler model - there is no need for multi-agency involvement, for example.

## Future extensions ##

The project scope is explicitly restricted to a proof of concept. Should the project proceed to a full system, there are a couple of related projects:
+ Plan Your Picnic (<http://planyourpicnic.org.au>) has been identified as the basis for a possible "front end" to the booking system to allow users to discover the most appropriate land for their use case.
+ More generally, the scoping process identified the desire to build a portal of mostly static information about the available public spaces in the ACT.

# Guidelines & Standards #

While the project is being developed, the project will be built in line with the following guidelines and standards:

+ Industry best practise for security and confidentiality, including the use of:
    + Secure Sockets Layer
	+ Storage of passwords using salts and a password based key derivation function rather than a simple hashing function.
	+ Use of parameterised queries to avoid SQL injection attacks.
	+ Use of proven frameworks over "in house" or DIY technologies.
+ Correct and valid use of technologies such as HTML and CSS, such that all pages pass W3C validation.
+ SSICT standards, such that a full solution can be hosted on SSICT infrastructure with a minimum of fuss.

Before the POC can be deployed, future work will be required to bring it in line with to following other standards:

+ WCAG 2.0 compliance, so as the system meets legislative/human rights requirements for accessibility.
+ ACT Government branding/visual identity

The POC will be developed in such a way as to make that future work as easy as possible.

# Ongoing Quality Control #

Firstly, the outputs are a proof of concept, so an output is "fit for purpose" inasmuch as it provides a realistic basis on which TAMS can evaluate the feasibility of converting the POC into a full system.

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

# Attachment: Functional Brief #

# Attachment: Technical Brief # 
