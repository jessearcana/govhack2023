Challenges:
- Highlight the diversity of South Australia's tourism product through gamification
  - How can we apply gamification to engage and educate young (South) Australians about South Australia's diverse tourism product offer and through this, influence key decision makers in their household to discover more of South Australia?
- Increase visitor expenditure through Smart Tourism
  - How can we use digital technology to "upsell" to visitors to South Australia by uncovering additional attractions and experiences and/or extending their stay?

Primary flow (general):
 - image and other data is indexed
 - search allows similarity on a few dimensions eg:
   - visually similar generally
   - contains similar visual elements (people, buildings, animals etc)
   - Activities for a trip plan

Why? Problem statement and/or Value proposition
- Current solutions:
  - travel agent
  - Pinterest
  - Friend's Facebook/insta/etc.
  - Angus' mastodon server
  - SA govt promotions like travel vouchers

User flow (tourism or maybe also remix):
- Admin user defines some basic parameters - eg tourism drive in South Australia
- End users land on a web page that gives an initial impression of the potential value based on admin params and maybe other users' feedback.
- Get customisation data:
  - About end user : Family of 4, kids genders and ages (unstructured and optional)
  - About end user desires relevant to to admin params : (outline of some holiday plans)
  - Some exemplar content : (highlights from previous holidays)
- Generate a story selling a hypothetical tailored holiday
  - Start with basic text
  - Could add:
    - voice-over
    - images
    - video
    - GenAI could even embed the end users or a likeness in the media that's generated.
- Pull out some key activities, places, accommodation, travel etc that can be matched with a pre-populated list of vendors or similar points of contact. (Backend only)
- Present the user with a list of likely contact items related to the story.
- Generate a trip planner map using the existing GET endpoint.
- For each point of interest on the map, fuzzy matching and generative AI summarisation might add some tips like best time to visit, events to watch out for, warnings, highlights etc from places reviews.


Gamification ideas:
 - Customise a trip plan and get points when people like it.