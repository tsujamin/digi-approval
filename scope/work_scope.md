% Digital Canberra Challenge -- Project Scope
% DigiACTive Pty Ltd (ABN 62 166 886 871)
% 28 November 2013

# Project Overview #
DigiACTive intends to construct a workflow-based system for use in event permit application, assessment and approval. In the proposed design, a workflow refers to a series of steps, each with certain criteria and a completing/approving party, that are used to model approval processes. The system will be provided as a browser-based application built on a framework of highly portable open source technologies. 

Within the system, several roles and interfaces exist to serve the needs of different stakeholders.

 * **Adminstrators** of the system will be able to modify and implement new workflows in-browser without the need to write additional code
 * **Customers** will be provided with an interface allowing new applications to be lodged, pending applications continued and completed applications reviewed
 * **Managers** have the power to delegate the processing of customers' applications to various **Reviewers** within the appropriate area

The system will provide flexibility for modifying workflows to adapt to changing business rules and processes, improved consistency in the review and assessment process, and can act as a **one-stop permit shop** for both customers and directorates. A more detailed description of the system's workflow model and software stack can be found in the initial pitch outline.

# Stakeholders #
## Territory and Municipal Services (TAMS) ##
The current public unleased land permit approval process falls under the jurisdiction of the **Licensing and Compliance Section, Parks and City Services Division** within the **Territory and Municipal Services Directorate (TAMS)**. Other units within TAMS also play a role in the approval process -- their requirements are similar to those for **Other Government Agencies** described below. In a production environment, TAMS Licensing and Compliance would be the primary Government user of the system and hold primary administrative and budgetary control over the system. At present, TAMS manages permits using a number of legacy systems which inhibit effective processing of applications. During the consultation process, TAMS have identified a number of requirements, based on their experience with legacy systems, which have been taken into account and will be implemented where possible.

## Shared Services ICT (SSICT) ##
**Shared Services ICT (SSICT)** is responsible for hosting and maintaining the ACT Government's ICT systems. SSICT has a number of policies and procedures in place regarding the Government's software configuration. In a production environment, SSICT would most likely be responsible for hosting and administering the system, and as such the system would be required to comply with these policies. In defining the scope of the project, SSICT's requirements have been taken into account.

## Other Government Agencies ##
The permit approval process involves several government agencies, including the **Emergency Services Agency**, the **Australian Federal Police**, the **ACT Insurance Authority** and the **Environment Protection Authority**. Each agency is responsible for ensuring that applications meet the relevant requirements within the agency's areas of interest. Each agency has its own policies, procedures and systems for handling applications. The system will be designed so as to allow agencies to communicate effectively with TAMS and customers, approving or denying relevant sections of applications where necessary.

## Customers ##
The system's customers include individuals, community organisations, businesses and other government agencies, who are collectively responsible for submitting more than 2,500 permit applications per year. Customers have an expectation of high-quality service from the Government, and have the right to a timely and fair decision on their permit applications. The system should ensure the permit application process is as simple and efficient as possible from the customer's point of view.

This project was submitted as part of the **Digital Canberra Challenge** by a community group, MusicACT, which organises public events on a regular basis. Whilst we have yet to engage in community consultation, we intend to collect and incorporate their feedback during the project's design phase.

# Inclusions #
The project's specific inclusions fall into two distinct categories: those which were initially pitched and those that, through consultation with stakeholders, were identified subsequently. The priority of the team is to produce a prototype demonstrating the advantages and strengths of a workflow based system within the challenge timeframe. What follows is a list of functionality inclusions that are considered **"in scope"** of the project but it must be noted that not all may make it into this iteration of the system.

## Initial Proposal Inclusions ##
+ The system will be modeled on workflows with various stages. Stages can involve the customer providing relevant documents, can lapse or continue after a specified period of time and can contain sub-workflows. Transitioning from one stage to another can emit notifications to the appropriate parties.
+ Administrators will be provided with a management interface where workflows can be created and modified. Such workflows will be rendered as flowcharts for comparison and verification against the corresponding directorate procedures.
+ Managers will be provided an interface which summaries pending applications and allows them to be assigned to a relevant and available approver.
+ Approvers will be provided an interface where they can communicate with and view/process the application of their customers.
+ Customers will be provided a portal displaying the status of their pending applications, providing a contact point with their assigned approvers, a archive of their previously completed applications and a list of potential applications they could begin to lodge.
+ In order to protect the integrity of the approver's computer system, any electronic documents lodged with the system will be stored and scanned for malicious content before becoming available for viewing.
+ A rigorous user authentication system will be implemented which, alongside a strict authorisation system, restricts the privileges and access rights of users to the appropriate sections of the system.
+ The system will provide confidentiality and security to users through the use of the Secure Socket Layer (SSL) cryptographic protocol.

## Consultation Based Inclusions ##
### Multiple Stakeholder Approval Management ###
The consultation period showed us that a major component in the current permit application process is seeking approval from the relevant stakeholders (e.g. AFP, ESA, ACTIA). This requires inter-agency communication, can result in the customers application requiring modification and in some cases such requests may go unanswered by the relevant agency. Ideally the proposed system will help alleviate problems arising from stakeholder approval using the following methods:

+ The system will provide the opportunity for workflow stages to automatically identify relevant stakeholders.
+ Upon receiving an application, an approver will be able to refer sections of it to the relevant stakeholders. 
+ Ideally this referral would remain in-system with the section being added to the pending applications of the stakeholder. 
+ For cases where the stakeholder is not a configured member of the system manual email contact will be available.
+ Notifications can be emitted to the stakeholder and approver in the case of non-respondance.

### Reporting and Querying Facilities ###
Our consultation also introduced us to the current system where querying of the database is readily available and reports used for distribution could be easily generated. Ideally our system would provide similar functionality as not to disrupt current organisational practices.

### Soft Warnings Regarding Optionality and Processing Time ###
Currently a reasonable amount of correspondence between customers and TAMS/PACS occurs in relation to whether a permit application need be lodged; consuming valuable processing time. There are also cases where customers lodge applications short of time and within the reserved application processing period of 28 days. This can result in dissatisfaction when approval is not received before the event date. In both of these cases the system may provide a soft warning to the user informing them or warning them of these circumstances; resulting in reduced workload for approvers

### Payment Systems ###
Several application varieties currently require payment of some variety. As such the system must provide facilities for workflows to require financial payment at certain stages.

# Exclusions #
The following serves to document those ideas and concepts discussed in the planing workshop and in subsequent consultation that are considered exclusions of the current project. The system as implemented in this stage of the project excludes:

+ Automatic assessment of the appropriateness of an event in a given location.
+ The management of land availability and booking calendar for use by customers during the application process. 
+ While payment integration will be a consideration during the development, specific integration with the ACT Government's current payment gateway will not be developed. 
+ The system will not serve as a general information portal regarding the territories public land and facilities. This is excluded due to such a portal being general and static enough that it could be developed separate to this system at a different time.

# Considerations #
While the following requirements and functionality may not be implementable in the system prototype, they will be kept as considerations during the design and development stages of the project:

+ A fully deployed system would, in the future, likely be extended to incorporate permit applications such as those for waste-skip placement and land development.
+ The deployed system would require integration with several of the territories current systems, such as the TRIM document management system and the ACT Government payment portal.
+ It is the desire of several project stakeholders that the future system would serve as a land booking availability portal also. A future cross-integration with the "Booking a government service" challenge was mentioned in passing as a possibility.
+ As a fully implemented system would likely reside on SSICT infrastructure the system must follow their deployment guidelines. At the present time the majority of the software stack adheres to these guidelines and due to the modular nature of the system the remainder (specifically the DBMS and deployment operating system) should be easily transferable. 

# Milestones #  
Coinciding with the development stage of the system we propose the following set of milestones. They are primarily those proposed in the original pitch adjusted to match the periods agreed to during the kick-off workshop. 

## 1. Implement a Event Permit Application System with a pre-configured workflow (12/12/13 - 11/1/14) ##

## 2. Pilot test the Milestone One implementation of the system with relevant stakeholders (11/1/14 - 18/1/14) ##

## 3. Implement dynamic workflow functionality within the Event Permit Application System (18/1/14 - 19/02/14) ##