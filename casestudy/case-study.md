# Digital Canberra Challenge: Round 1 - Case Study
## DigiACTive Pty Ltd, March 2014

# Executive Summary


# Description of challenge
**What was in the scope?**

## Background
A thriving, vibrant city should make it easy for citizens and small businesses to run public events. At the same time, regulations and permit systems are needed to make sure that events are run in a safe, community-friendly and sustainable way.

Unfortunately, the proliferation of regulations and permits has made running events into something more akin to navigating a maze. The point of this challenge is to provide Canberrans with a simple, efficient way to navigate that maze.

## Our solution: a birds-eye view
Our proof-of-concept system demonstrates a system to provide residents and businesses with a clear, streamlined way to navigate the various approvals required. The system provides a central point of contact so that, as far as possible, a single public servant sees the process through from start to finish and is able to help resolve problems as they come up. The system lay out the requirements clearly, helping directorates to ensure that applicants understand what is required of them and can meet those requirements with a minimum of fuss.

## The scope of our system
As a proof of concept, the system necessarily has a restricticted scope.

Include in the scope was:

# Methodology
**How did the team address the challenge?** (NB: this is not the same as the proposed solution. It's asking ... how we got there?)

 * Saw the challenge, rallied troops in CSSA. ended up with a group of 3.
 * ... germ of an idea: background in FSM, read an article about FSM v workflow engines. Saw the challenge, went: "Hmm, that might work."
 * Research: is that implemented in public source code? Yes
 * Can I wrap that in an open-source stack? Yes
 * How do we make this scale? Make sure things disaggregate nicely.
 * Let's test the concept: submit pitch, do verbal pitch
 * Let's refine the concept: meetings with Fleur, etc.
 * Let's build the concept
 * Repeat - test, refine, build

Acknowledge the excellent work of RR, and the project board generally in keeping us on track.

# Proposed solution
**technical description of prototype; how does this (solution) add to Canberra becoming a digital city**

## The prototype in overview

### The core: Workflow Engine

### Customer experience

#### Regular citizens

#### Community groups

### Directorate experience 

 * Approver
 * Delegator

### Baked-in flexibility

 * Point and click workflow design.

## The prototype: Tech Specs
 * not just what we used but why, and why it was awesome.

## Making Canberra a digital city

We need to tie into this stuff: http://www.cmd.act.gov.au/policystrategic/digitalcanberra

The more we can do this the better.


# Production system
**address sustainability, scalability, integration, (approx.) cost**

The system has been designed with production in mind.

## Sustainability
Our system is sustainable from a number of different angles. In particular, we have focused on **sustaining the capacity of the system to function as desired**, in particular by reducing dependence on the DigiACTive team.

 + ... directorates - they don't depend on us to set things up

### Implementation of the system within directorates
Because of the point-and-click workflow editor, the system can be implemented across directorates without needing the DigiACTive team's intervention.

### Ongoing use of the system within directorates
The system is designed to be tolerant to changes in staffing within a directorate.
 + The delegator/approver system provides a simple approach to re-allocating work as staff arrangements change. (TODO: a production system would need a "don't allocate more tasks to this approver" button) It provides direct visibility into the workload of approvers, and allows it to be adjusted as needed.
 + The system is also designed to be sustainable in the sense that it's integrity is not threatened when staff members leave. Each staff member has an individual user account, which can be easily deactivated when they leave.

The system is also designed to be tolerant to changes in business processes: the point-and-click editor enable these changes to be reflected in the workflow models "in house", without requiring DigiACTive to write any code.

 + ... improved sustainability of community organisations

### Ongoing use within community organisations
A major complaint that drove the challenge was the need to reduce the duplicated effort that occurs when a community group runs similar events repeatedly.

The differentiated registration for community groups is designed to maintain their capacity in the face of changing membership.
 + It allows group membership to change without losing any information: when a group member leaves the group, they do not take any information with them. All applications made on behalf of the community group stay on archive and are accessible to members of the group.
 + It maintains the integrity of the community group's application process: once a member leaves or is removed from the group, they can no longer take actions on behalf of the group.

 + ... developers - open stack and toolset

### Sustainable software stack and toolset

The system has been designed and built such that if the DigiACTive team were hit by a bus, it would be possible to hire replacement staff that could quickly come up to speed on the system.

To that end:
 + The system is built on widely used, open source software, as detailed in the technical specs. 
 + Our implementation has consistently preferred to integrate prebuilt software packages rather than reinvent the wheel. This means:
    * Our code conforms to the convetions required by those packages.
    * Our code base is small - only implementing those things not implemented in other software.
 + We have a unit test suite.

#### Contributing to the open-source ecosystem
As we have built on open-source software, we have often found that we need to fix a particular bug or extend a particular feature in the software we are using. We have consitently sought to contribute these changes back. This has a number of benefits:
 + It contributes to the open-source eco-system, which we in turn benfit from.
 + It shifts the responsibility for maintaining our changes away from us and back to the original maintainer of the package, reducing our ongoing workload.

 + ... growing requirements - flexibility and power, generic design

### Sustainable software
The system is designed to remain viable in the face of changing requirements.

## Scalability

 + ... technically - decoupled design, everything easily disaggregates and multiplies.
 + ... across directorates - authentication system allows multiple directorates to use shared system: not only will they not step on each others toes, with subworkflows they will complement each other.
 + ... 

## Integration

 + ... reporting
 + ... existing workflows - modelling rather than replacing.

## The bottom line

# Concluding remarks
**experience of the team's involvement in the competition; feedback/suggestions for next rounds**

The team came together from a group of friends at the Australian National University. We were not a pre-established company, but formed a proprietary limited company after progressing to the bake-off stage of the competition. While some of us had experience consulting in the private sector, none of us had worked with the public sector.

There are two main observations arising from our position.

### 1: Commercialisation

We entered the competition as a group of friends. In order to proceed in the bake-off, we required a formal legal structure. We consulted a lawyer, and opted to form a proprietary limited company. We were also required to acquire insurance as part of the bake-off agreement.

We found the administrative process of forming a company, getting the necessary insurance, and sorting out the necessary legal documents to be immensely educational. On the other hand, we also found it to be incredibly time-consuming, expensive and frustrating. It consumed the bulk of our time for the first several weeks of the competition, and consumed well over half of (TODO more accurate %age) our total project budget.

If we had an pre-existing company, we could have redirected our time and money towards a number of different things. For example, if we had been less pushed for time and money, we would have brought a graphic designer and a user experience specialist on board.

On the plus side, being pushed to have a formal legal structure has set us up well to continue the project into the future. On the down side, if we choose not to proceed, we have to wrap up the company, sort out its tax affairs, and so on: we're left holding a time-consuming liability.

We have a number of suggestions for future competitions:
 + Starting a company is not a straightforward process. We were fortunate to have team members with experience as sole traders and in forming incorporated associations, which helped, but we would have benefited from some sort of information session or infomation pack outlining matters such as:
  + different business structures: e.g. company vs partnership
  + how to go about forming one: applying directly through ASIC v applying through e.g. MYOB CompanyDocs,
  + the legal agreements needed to protect us, e.g. a Shareholders' Agreement
  + the various different types of insurance we would require
  + how we would go about expanding or winding up a company after the competition

 + SMEs have a disinct advantage compared to other entrants because of their existing company status: they don't need to spend any of their budget on forming a company. It may be worth considering evening out this advantage.
 
 + The insurance requirement could be re-evaluated. We were requried to hold professional indemnity insurance to guard against direct loss to the government. However it is hard to see how the proof of concept could actually cause the government financial loss, given that it was not hosted on government servers, did not process payments, and did not process actual user data. TODO: the insurance will actually be really, really useful iff we proceed.


### 2: Public Sector thinking

A major thing we had to adapt to is the very different way of thinking in the government space versus the innovation/start-up space.

The process we had was very linear: gather requirements, develop a design document, build the system. This is in sharp contrast to the way we are used to operating: build a prototype, present it, see how people actually use it and what they want changed, fix the prototype in response, get more feed back and so on. We would have attempted to build a minimum viable product by iteration rather than through explicit design.

**How has this worked out in practise? What was good/bad about doing it the government's way?**

 * Feedback is less interactive than we're used to. We don't get to just sit down with the people and watch how they use it. We may have ended up blocking on feedback which would have been terrible.

#### What's in a name?
Manager v delgator (even receptionist) -> we're not used to the technical business meanings.


# Other remarks

## Suggestions for future teams coming from non-commercial environments.

 * One of our biggest and most surprising time-sinks arose from the different hardware we had. 2 of our members had MacBooks, and one had a laptop running some variant of Linux. Despite our best efforts to make the development environment consistent through the use of Vagrant, we found a lot of time still diappeared in the differences Vagrant couldn't quite smooth out. **It's worth getting identical systems somehow**: either by buying identical hardware, or by doing all your development in the cloud from the start.

 * It's very tempting to not name a leader, especially as a group of friends. However, *there are no leaderless groups*: someone will end up leading; sometimes different people at different points, but someone must take the lead for things to get done. We would have benefitted from picking a leader at the start, and would advise future groups to do so.
