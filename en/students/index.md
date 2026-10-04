---
title: For Students
ref: students
nav:
  order: 5
  tooltip: Information for student researchers
---

# {% include icon.html icon="fa-solid fa-graduation-cap" %}For Students
{: .page-title }

An overview of foundational study, the research process, and goals for each degree at SEARCH Lab.
{: .page-intro }

{% include section.html %}

## Research Goals and Supervision

SEARCH Lab guides students in defining and solving space mission design problems independently. Students begin with theory and practical analysis, then compare designs against mission requirements and assess their feasibility.

## Foundational Study and Practical Analysis

Students begin with theory and analytical methods suited to their background and interests. Study covers the areas below, with topics and their sequence adjusted to the student's research.

{% for method in site.data.research-topics.methods -%}
- **{{ method.en.title }}**: {{ method.en.study }}
{% endfor %}

Students use Python, MATLAB, STK, and GMAT as appropriate to the problem. They learn numerical integration and write analysis and simulation code, working through problems in orbit propagation, orbital transfers, communications visibility, trajectory optimization, and control simulation. They check both their results and the assumptions behind their models.

## Choosing and Developing a Research Topic

Students choose a topic with their advisor, considering their interests, preparation, the lab's research direction, and available projects. They draw on the lab's [core theories and methods]({{ '/en/research/' | relative_url }}#methods) to identify research questions in the areas below.

{% for topic in site.data.research-topics.applications -%}
- [{{ topic.en.title }}]({{ '/en/research/' | relative_url }}#{{ topic.id }})
{% endfor %}

For example, a project might compare coverage and revisit intervals for different satellite counts and constellation configurations, or evaluate contact opportunities and data return for deep-space optical communications.

In [attitude dynamics and control]({{ '/en/research/' | relative_url }}#attitude-dynamics-control), a project might examine how solar-sail attitude errors affect trajectory tracking. In [AI and machine learning applications]({{ '/en/research/' | relative_url }}#ai-machine-learning), it might compare the accuracy and computation time of learning-based control and conventional optimal control.

Once a topic is selected, students review the literature and carry out preliminary analysis to set their objectives and performance metrics. They build analytical and simulation models, examine how design variables affect performance, and document their findings, including validation and limitations.

## Research Projects and In-Space Demonstration

Student researchers work on topics linked to national R&D programs and deep-space exploration projects at the Korea Aerospace Research Institute (KARI). Depending on their research topic and the project schedule, they contribute to mission design, systems analysis, performance verification, flight operations concepts, simulation models, and technical documentation.

For CubeSat-class satellites and in-space demonstration missions, students take part in hardware fabrication, ground environmental testing, operational scenario development, and in-orbit performance verification. Their involvement depends on the development stage and their assigned work. They learn how design and analysis inform fabrication, testing, and operations.

## Research Goals by Degree

Research scope and depth vary by degree, with the following goals.

{: .students-degrees role="list" }
- **Master's students** define a research question in space mission design, orbit analysis, guidance and control, or a related area. They apply appropriate analytical methods, validate their results, and write a thesis. They aim to present at conferences and submit journal articles during their studies.
- **Doctoral students** identify an original question arising from limitations in existing work and pursue it independently. They propose new mission design methods, analytical procedures, or system design concepts, and assess their contribution and applicability.

Depending on the topic and type of work, students document their results in theses and dissertations, conference presentations, journal articles, technical reports, mission design documents, and simulation code. They record model assumptions, analytical procedures, and validation evidence so that others can understand and review their findings.

Writing guidance is grounded in research ethics, including proper citation and accurate reporting of results. Students learn how to structure and write a paper, working through drafts and revisions to explain their research objectives, methods, results, and limitations clearly.

{% include section.html %}

## Textbooks and Reference Materials

The textbooks and papers below are references for foundational study and research. Students select readings according to their background and research topic.

Textbooks include a print ISBN-13, a book information link, and an Amazon search link. Papers and online resources link to a DOI or the original source.

### Orbital Mechanics and Astrodynamics

{% include references/astrodynamics.md %}

### Space Mission Design and Systems Engineering

{% include references/mission-design.md %}

### Optimization and Optimal Control

{% include references/optimal-control.md %}

### Planetary Entry, Descent, and Landing

{% include references/edl.md %}

### Solar Sails and Low-Thrust Deep-Space Missions

{% include references/solar-sail.md %}

### Deep-Space Optical Communications

{% include references/optical-communications.md %}

### Space Agency Technical Documents and Research Papers

{:start="22"}
22. Mission design documents, technical reports, system requirements documents, and related research papers from space agencies such as NASA, ESA, JAXA, and KARI.
