---
title: For Students
ref: students
nav:
  order: 5
  tooltip: Information for student researchers
---

# {% include icon.html icon="fa-solid fa-graduation-cap" %}For Students
{: .page-title }

Learn about foundational study, the research process, and degree-level goals for students at SEARCH Lab.
{: .page-intro }

{% include section.html %}

## Research Goals and Supervision

SEARCH Lab helps students develop the ability to define and solve space mission design problems independently. Starting with theory and practical analysis, students learn to interpret mission requirements, compare design alternatives, and use their results to assess mission feasibility.

## Foundational Study and Practical Analysis

Early study builds on each student's academic background and research interests. The main areas are listed below; specific topics and their sequence are adapted to the student's research.

- **Orbital mechanics and astrodynamics**: the two-body problem, orbital elements, orbital transfers and perturbations, satellite orbit analysis, and spacecraft trajectory design
- **Mission design and spacecraft systems**: mission architecture, satellite and exploration spacecraft systems, mission requirements analysis, and concepts of operations
- **Numerical analysis and programming**: numerical integration, optimization and optimal control, and implementation of analytical models and simulation code

Students use Python, MATLAB, STK, and GMAT as appropriate to the problem. Exercises in orbit propagation, orbital transfers, communications visibility, and orbit and trajectory optimization help students learn to assess model assumptions and check whether their results are valid.

## Choosing and Developing a Research Topic

Students choose a topic in discussion with their advisor, considering their interests and preparation, the lab's research direction, and available projects. They draw on astrodynamics and high-fidelity orbit analysis, dynamical systems and multi-body astrodynamics, numerical optimization and optimal control, and mission architecture and systems analysis to develop specific questions in the following areas.

{% for topic in site.data.research-topics.applications -%}
- [{{ topic.en.title }}]({{ '/en/research/' | relative_url }}#{{ topic.id }})
{% endfor %}

For example, a project might compare coverage and revisit intervals for different satellite counts and constellation configurations, or evaluate contact opportunities and data return for deep-space optical communications. Follow each link for details of the research area.

Once a topic is selected, students refine their objectives and performance metrics through literature review and preliminary analysis. They then build analytical and simulation models, examine how design variables affect performance, and document the validity and limitations of their results.

## Research Projects and In-Space Demonstration

Student researchers conduct research linked to national R&D programs and deep-space exploration projects at the Korea Aerospace Research Institute (KARI). Their research topics and project schedules determine the scope of their involvement and responsibilities. Assigned work includes mission design, systems analysis, performance verification, development of flight operations concepts, simulation model development, and technical documentation.

In CubeSat-class satellite development and in-space demonstration missions, students gain experience in hardware fabrication, ground environmental testing, operational scenario development, and in-orbit performance verification according to the development stage and their assigned responsibilities. These activities help students understand how design and analysis lead to fabrication, testing, and operations.

## Research Goals by Degree

The scope and depth of research reflect the degree being pursued, with the following goals.

{: .students-degrees role="list" }
- **Master's students** define a focused question in space mission design or orbit analysis, apply appropriate analytical methods, and obtain and validate results. They develop this work into a thesis and aim to present at conferences and submit journal articles during their studies.
- **Doctoral students** identify an original research question based on limitations in existing work and pursue it independently. They aim to propose new mission design methods, analytical procedures, or system design concepts, and assess their contribution and applicability.

Depending on the topic and type of work, results are documented in theses and dissertations, conference presentations, journal articles, technical reports, mission design documents, and simulation code. Students learn to explain their findings and record model assumptions, analytical procedures, and validation evidence so that others can review their work.

{% include section.html %}

## Textbooks and Reference Materials

These resources support study from foundational theory to advanced research topics. Students select relevant textbooks and papers according to their academic background and research topic, and consult them as their study and research progress.

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
