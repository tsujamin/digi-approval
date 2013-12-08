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

+ **Conflict in requirements/direction from stakeholders** TODO
    + TAMS/community groups pushing in different directions due to different foci, pain points.
    + Reasonably likely in feedback stage.
    + Ultimately a governance issue?

+ **DigiACTive team newness/inexperience leading to poor performance**
    + *Likelihood*: Moderate.
    + *Severity*: Potentially severe.
    + *Evaluation*: Managed through the Digital Canberra Challenge/Collaborative Agreement governance structure.


### Management Plan: unexpected technical difficulty ###

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

## Future extensions ##

The project scope is explicitly restricted to a proof of concept. 

### Extend project ###

### Integrate "Plan Your Picnic" material: Google Maps frontend ###

# Guidelines & Standards #

Now:

+ SSL
+ SSICT standards

Future work:

+ WCAG 2.0 compliance (accessibility)
+ ACT Government branding/visual identity

# Project Closure and Evaluation #

+ It's finishing at 1 Mar whether we like it or not.
+ DCC evaluation
+ TAMS internal evaluation - "gate" for go/no-go of next stage

# Attachment: Functional Brief #

# Attachment: Technical Brief # 
