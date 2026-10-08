---
title: Research
ref: research
nav:
  order: 2
  tooltip: Research areas
---

# {% include icon.html icon="fa-solid fa-rocket" %}Research
{: .page-title }

SEARCH Lab builds on astrodynamics and dynamical systems theory to design **space mission architectures** spanning Earth orbit and deep-space exploration. We combine orbit and trajectory analysis, guidance and attitude control, numerical optimization, AI and machine learning, and systems analysis to assess mission feasibility and study approaches to in-space demonstration.
{: .page-intro }

<nav class="research-nav" aria-label="Research areas">
  <a href="#methods">Theories &amp; methods</a>
  <a href="#earth-orbit">Earth-orbit missions</a>
  <a href="#planetary">Lunar &amp; planetary missions</a>
  <a href="#entry-systems">Entry, landing &amp; thermal protection</a>
  <a href="#solar-sail">Solar sails</a>
  <a href="#optical-communications">Optical communications</a>
  <a href="#cubesat">CubeSats &amp; demonstration</a>
</nav>

{% include section.html %}

## Core theories and methods {#methods}

<div class="research-methods" markdown="1">

{% for method in site.data.research-topics.methods %}
<div class="research-method" markdown="1">

{% for alias in method.aliases %}<div id="{{ alias }}" aria-hidden="true"></div>{% endfor %}

<div class="research-method-number" aria-hidden="true">0{{ forloop.index }}</div>

### {{ method.en.title }} {#{{ method.id }}}

{{ method.en.summary }}

</div>
{% endfor %}

</div>

{% include research-figure.html topic="architecture" caption="Starting from mission objectives and constraints, we analyze and optimize a coupled model of trajectories, systems, and communications operations, then assess feasibility to refine the design." alt="Mission objectives and constraints feed a coupled model of trajectories and maneuvers, spacecraft and payload, and links and operations. Performance, feasibility, sensitivity, and risk assessments feed back into the design." %}

{% include section.html %}

## Research applications {#applications}

We apply these core theories and methods across six areas, addressing the mission environments and technology requirements specific to each.

### {% include icon.html icon="fa-solid fa-globe" %}{% include research-title.html id="earth-orbit" %} {#earth-orbit}

We design Earth-orbit missions for observation, communications, and technology demonstration. We assess orbits and operations scenarios against mission requirements and analyze coverage, revisit intervals, and ground station visibility.

- Orbital altitude, inclination, and concepts of operations for observation, communications, and technology demonstration satellites
- Regional coverage, revisit intervals, and ground station contact opportunities
- Long-term orbit propagation and maintenance strategies accounting for Earth's nonspherical gravity and atmospheric drag

#### Satellite constellation design {#earth-constellation}

For missions involving multiple satellites, we design satellite count, orbital plane configuration, and satellite phasing together. We optimize the constellation by analyzing trade-offs among observation and communications performance, propellant use, and operational effort, and assess long-term performance under orbital perturbations and orbit maintenance maneuvers.

For formation flying that requires precise relative positioning, we extend this work to [guidance and control](#guidance-control) using relative orbit dynamics and accounting for navigation errors.

{% include research-figure.html topic="earth-constellation" caption="Illustrative constellation with satellites distributed across three orbital planes. Colors distinguish the planes; satellite sizes and orbital altitudes are not to scale." alt="A schematic of satellites distributed across three circular orbits around Earth, with altitude, inclination, orbital planes, and satellite phasing identified as design variables." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-moon" %}{% include research-title.html id="planetary" %} {#planetary}

We design lunar and planetary exploration missions, including lunar landers and Mars orbiters and landers. We assess orbits and landing sites against exploration objectives, then examine how the relative positions of spacecraft, observation targets, and Earth affect observations, communications, and operations.

- Conceptual design of lunar exploration and landing missions and Mars orbiter and lander missions
- Orbit and landing site assessment against exploration objectives
- Observation and communications geometry between spacecraft, surface targets, and Earth
- Spacecraft operations scenarios based on observation and contact opportunities

{% include research-figure.html topic="planetary" caption="The relative positions of an orbiter, surface targets, and Earth help determine observation opportunities and communications paths. Sizes and distances are not to scale." alt="A conceptual diagram showing an orbiter, a surface target, and Earth, with observation directions and communications paths between them." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-parachute-box" %}{% include research-title.html id="entry-systems" %} {#entry-systems}

#### Planetary entry, descent, and landing {#edl}

We study how spacecraft enter an atmosphere, slow down, and land safely on planets such as Mars. Our work examines how atmospheric and aerothermodynamic conditions, parachute deployment, and guidance and control affect the trajectory and landing accuracy.

- Mars atmospheric entry trajectory and entry guidance analysis
- Parachute deployment conditions and deceleration and landing scenarios
- Three- and six-degree-of-freedom simulation with atmospheric and aerothermodynamic models
- Landing dispersion analysis and planetary landing mission performance assessment

{% include research-figure.html topic="edl" caption="Representative stages of Mars entry, descent, and landing. Atmospheric entry, parachute deceleration, final descent, and touchdown are designed together; the specific approach varies by mission." alt="A sequence showing atmospheric entry at Mars, parachute deceleration, final descent, and touchdown on the surface." %}

#### Earth re-entry and thermal protection systems {#reentry}

We analyze aerodynamic heating and deceleration loads as spacecraft and sample return capsules enter Earth's atmosphere at high speed. We study how to design and verify heat shields and other thermal protection systems by considering re-entry trajectories and thermal environments together.

- Re-entry trajectories, entry corridors, and recovery scenarios for sample return capsules
- Prediction of re-entry environments, including aerodynamic heating and deceleration loads
- Thermal protection system concepts and thickness sizing, and thermal response analysis of ablative and reusable materials
- Verification methods using ground tests, such as arc-jet testing, and flight tests

{% include research-figure.html topic="reentry" caption="A conceptual cross-section of a return capsule with an ablative heat shield. The heat shield and insulation limit heat transfer to the interior; layer arrangements and thicknesses depend on the materials and mission conditions." alt="A return capsule facing hypersonic flow, with its bow shock, heated gas layer, ablative heat shield, insulation, and internal payload identified." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-sun" %}{% include research-title.html id="solar-sail" %} {#solar-sail}

Solar sails generate thrust from solar radiation pressure as sunlight transfers momentum to the sail. We study how changing a sail's orientation alters its trajectory, and use this principle to design long-duration flights and future deep-space missions with reduced propellant needs.

- Astrodynamics accounting for solar radiation pressure and sail attitude
- Solar sail orbit raising and long-duration low-thrust trajectory design
- Non-Keplerian and other special orbits and future exploration mission concepts
- Solar sail in-space demonstration mission planning

{% include research-figure.html topic="solar-sail" caption="Sunlight transfers momentum to a sail, producing thrust. The right panel shows an ideal, perfectly reflecting sail in cross-section; sail orientation affects the magnitude and direction of thrust." alt="A deployed solar sail and a cross-section of an ideal reflective sail, showing incident and reflected light and thrust normal to the sail surface." %}

#### Integrated attitude and orbit control {#integrated-attitude-orbit-control}

We aim to combine [guidance and control](#optimization) with [attitude dynamics and control](#attitude-dynamics-control) to analyze and control coupled solar-sail orbit and attitude motion. We model solar radiation pressure forces and torques, including center-of-mass and center-of-pressure geometry, and assess mission feasibility through six-degree-of-freedom simulation with actuator limits and observation and communications pointing constraints. We also examine [AI and machine learning](#ai-machine-learning) for control command prediction and autonomous flight.

Related prior work: [Indirect methods for deep-learning-based solar-sail optimal control (2025, Korean)](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12589746)

#### Solar sail deployment mechanism: development and ground tests {#solar-sail-ground-test}

The Korea Aerospace Research Institute (KARI) developed a ground test model with a 10 m × 10 m (100 m²) sail to advance solar sail deployment technology for deep-space exploration. A motor extends four supporting booms to unfurl the stowed membrane. Ground tests identified deployment problems and opportunities for improvement. The videos show the test model deploying from overhead and side views.

Further reading: [KARI press release (Korean)](https://www.kari.re.kr/kor/article/ATCL87374b48c/18228) · [Tests and Lessons Learned of Solar Sail Deployment](https://doi.org/10.52912/jsta.2026.6.3.293)

<div class="research-video-grid">
{% include research-video.html id="sail-test-overhead" file="kari-solar-sail-deployment-overhead.mp4" poster="kari-solar-sail-deployment-overhead.jpg" title="Solar sail deployment · overhead view (23 s clip)" %}
{% include research-video.html id="sail-test-side" file="kari-solar-sail-deployment-side.mp4" poster="kari-solar-sail-deployment-side.jpg" title="Solar sail deployment · side view (22 s clip)" %}
</div>

#### Deorbiter for space debris removal: development and ground tests {#deorbiter-ground-test}

KARI developed a ground test model of a deorbiter to investigate technologies for capturing and removing debris from low Earth orbit. It combines towing, capture, and deployment mechanisms. The concept uses a 5 m × 5 m (25 m²) drag sail to increase atmospheric drag and bring captured objects toward re-entry. The videos show ground tests of the drag-sail deployment function.

Further reading: [KARI press release (Korean)](https://www.kari.re.kr/kor/article/ATCL87374b48c/18417) · [Deorbiter development and tests](https://doi.org/10.52912/jsta.2026.6.2.196)

<div class="research-video-grid">
{% include research-video.html id="deorbiter-test-wide" file="kari-deorbiter-drag-sail-wide.mp4" poster="kari-deorbiter-drag-sail-wide.jpg" title="Drag-sail deployment · wide view (2.4 s clip)" %}
{% include research-video.html id="deorbiter-test-overhead" file="kari-deorbiter-drag-sail-overhead.mp4" poster="kari-deorbiter-drag-sail-overhead.jpg" title="Drag-sail deployment · overhead view (12.9 s clip)" %}
</div>

{% include section.html %}

### {% include icon.html icon="fa-solid fa-satellite-dish" %}{% include research-title.html id="optical-communications" %} {#optical-communications}

Deep-space optical communications uses lasers to exchange data between spacecraft and Earth. Our interests focus on how trajectories, spacecraft attitude, distance from Earth, and ground station weather and atmospheric conditions affect link performance. We aim to evaluate contact opportunities and data return, and to develop system requirements, operations plans, and technology demonstration scenarios within mass, power, and thermal limits.

- Link budgets and data transmission performance under range, optics, power, and loss constraints
- Pointing, acquisition, and tracking (PAT) requirements and spacecraft attitude stability
- Ground station placement and link availability under atmospheric, weather, and visibility constraints
- Combined radio-frequency (RF) and optical operations, transmission scheduling, and technology demonstration scenarios

{% include research-figure.html topic="optical-communications" caption="A conceptual laser downlink from a spacecraft to a ground telescope. Distance, pointing error, atmospheric conditions, and contact time affect data transmission performance." alt="A laser downlink from a spacecraft terminal through the atmosphere to a ground telescope, showing range, beam spread, pointing loss, power and optics, weather and link availability, and contact time and data return." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-satellite" %}{% include research-title.html id="cubesat" %} {#cubesat}

We study how CubeSats can demonstrate mission concepts and technologies in space. Our interests span mission design, system requirements, ground testing, and in-orbit operations. Student researchers conduct research linked to relevant national R&D programs, with the scope of their involvement and responsibilities determined by research topics and project schedules.

- CubeSat-class mission concepts and system requirements definition
- Ground testing and qualification methods for the space environment
- Satellite concepts of operations and in-orbit technology verification scenarios
- In-space demonstration mission planning linked to national R&D programs

For [attitude control](#attitude-dynamics-control) and autonomous control algorithms, we consider verification from numerical simulation to ground tests integrating onboard computers, sensors, and actuators, and assess opportunities for in-orbit demonstration according to project scope and resources.

{% include research-figure.html topic="cubesat" caption="CubeSat development translates a mission concept into system requirements, progresses through design, fabrication, and ground testing, and verifies technologies during in-orbit operations." alt="A conceptual CubeSat development and verification sequence from mission concept through system design, fabrication, ground testing, and in-orbit operations and demonstration." %}
