# Digital Canberra Challenge: Round 1 - Case Study
## DigiACTive Pty Ltd, March 2014

# Executive Summary


# Description of challenge
**What was in the scope?**

A thriving, vibrant city should make it easy for citizens and small businesses to run public events. At the same time, regulations and permit systems are needed to make sure that events are run in a safe, community-friendly and sustainable way.

Unfortunately, the proliferation of regulations and permits has made running events into something more akin to navigating a maze. The point of this challenge is to provide Canberrans with a simple, efficient way to navigate that maze.

Our proof-of-concept system demonstrates a system to provide residents and businesses with a clear, streamlined way to navigate the various approvals required. The system provides a central point of contact so that, as far as possible, a single public servant sees the process through from start to finish and is able to help resolve problems as they come up. The system lay out the requirements clearly, helping directorates to ensure that applicants understand what is required of them and can meet those requirements with a minimum of fuss.

# Methodology
How did the team address the challenge?

# Proposed solution
technical description of prototype; how does this (solution) add to Canberra becoming a digital city



# Production system
**address sustainability, scalability, integration, (approx.) cost**

The system has been designed with production in mind.

## Sustainability
Our system is sustainable from a number of different angles:

 + ... directorates - they don't depend on us to set things up
 + ... developers - open stack and toolset
 + ... growing requirements - flexibility and power, generic design

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

 * It would have been good to spend money on equivalent hardware for all of us - so much lost time on AJD's linux box. (bindfs!)
 * There are no leaderless groups - we would have benefitted from picking a leader at the start.
