---
title: Research
ref: research
nav:
  order: 2
  tooltip: Research areas
---

# {% include icon.html icon="fa-solid fa-rocket" %}Research
{: .page-title }

SEARCH Lab draws on orbital mechanics and astrodynamics to design lunar, planetary, and deep-space exploration missions and study trajectory optimization and optimal control.
{: .page-intro }

<nav class="research-nav" aria-label="Research areas">
  <a href="#methods">Core methods</a>
  <a href="#planetary">Lunar &amp; planetary missions</a>
  <a href="#entry-systems">Entry, landing &amp; thermal protection</a>
  <a href="#solar-sail">Solar sails</a>
  <a href="#optical-communications">Optical communications</a>
  <a href="#cubesat">CubeSats &amp; demonstration</a>
</nav>

{% include section.html %}

## Core Research Methods {#methods}

<div class="research-methods" markdown="1">

<div class="research-method" markdown="1">

### {{ site.data.research-topics.methods[0].en.title }} {#architecture}

We translate exploration goals into mission and system requirements and concepts of operations, then analyze the interactions between trajectories, spacecraft, communications, and landing constraints. Conceptual design and trade studies help us assess mission scenarios linked to national space development programs.

</div>

<div class="research-method" markdown="1">

### {{ site.data.research-topics.methods[1].en.title }} {#dynamical-systems}

We aim to compute phase-space structures, such as periodic orbits around the Lagrange points and their invariant manifolds, in multi-body models like the circular restricted three-body problem. These structures will help us systematically explore the design space of low-energy transfers and non-Keplerian orbits and provide initial guesses for high-fidelity orbit analysis.

</div>

<div class="research-method" markdown="1">

### {{ site.data.research-topics.methods[2].en.title }} {#astrodynamics}

We propagate orbits with high-fidelity models of gravity and orbital perturbations to analyze spacecraft motion. We assess the feasibility and performance of lunar and planetary transfers, orbit insertion, and maneuver strategies under realistic mission conditions.

</div>

<div class="research-method" markdown="1">

### {{ site.data.research-topics.methods[3].en.title }} {#optimization}

We use numerical optimization, optimal control, and sensitivity analysis to examine trade-offs among launch dates, flight time, propellant use, communications, landing accuracy, and mission risk. We study trajectories and control strategies for low-thrust and continuous-thrust transfers, landing guidance, and deceleration.

</div>

</div>

{% include research-figure.html topic="architecture" caption="Starting from mission objectives and constraints, we analyze and optimize a coupled model of trajectories, systems, and communications operations, then assess feasibility to refine the design." alt="Mission objectives and constraints feed a coupled model of trajectories and maneuvers, spacecraft and payload, and links and operations. Performance, feasibility, sensitivity, and risk assessments feed back into the design." %}

{% include section.html %}

## Research Applications {#applications}

We apply these shared methods across five areas, addressing the mission environments and technology requirements specific to each.

### {% include icon.html icon="fa-solid fa-moon" %}{{ site.data.research-topics.applications[0].en.title }} {#planetary}

We design lunar and planetary exploration missions, including lunar landers and Mars orbiters and landers. We assess orbits and landing sites against exploration objectives, then examine how the relative positions of spacecraft, observation targets, and Earth affect observations, communications, and operations.

- Conceptual design of lunar exploration and landing missions and Mars orbiter and lander missions
- Orbit and landing site assessment against exploration objectives
- Observation and communications geometry between spacecraft, surface targets, and Earth
- Spacecraft operations scenarios based on observation and contact opportunities

{% include research-figure.html topic="planetary" caption="The relative positions of an orbiter, surface targets, and Earth help determine observation opportunities and communications paths. Sizes and distances are not to scale." alt="A conceptual diagram showing an orbiter, a surface target, and Earth, with observation directions and communications paths between them." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-parachute-box" %}{{ site.data.research-topics.applications[1].en.title }} {#entry-systems}

#### Planetary Entry, Descent, and Landing {#edl}

We study how spacecraft enter an atmosphere, slow down, and land safely on planets such as Mars. Our work examines how atmospheric and aerothermodynamic conditions, parachute deployment, and guidance and control affect the flight path and landing accuracy.

- Mars atmospheric entry trajectory and entry guidance analysis
- Parachute deployment conditions and deceleration and landing scenarios
- Three- and six-degree-of-freedom simulation with atmospheric and aerothermodynamic models
- Landing dispersion analysis and planetary landing mission performance assessment

{% include research-figure.html topic="edl" caption="Representative stages of Mars entry, descent, and landing. Atmospheric entry, parachute deceleration, final descent, and touchdown are designed together; the specific approach varies by mission." alt="A sequence showing atmospheric entry at Mars, parachute deceleration, final descent, and touchdown on the surface." %}

#### Earth Re-entry and Thermal Protection Systems {#reentry}

We analyze aerodynamic heating and deceleration loads as spacecraft and sample return capsules enter Earth's atmosphere at high speed. We study how to design and verify heat shields and other thermal protection systems by considering re-entry trajectories and thermal environments together.

- Re-entry trajectories, entry corridors, and recovery scenarios for sample return capsules
- Prediction of re-entry environments, including aerodynamic heating and deceleration loads
- Thermal protection system concepts and thickness sizing, and thermal response analysis of ablative and reusable materials
- Verification methods using ground tests, such as arc-jet testing, and flight tests

{% include research-figure.html topic="reentry" caption="A conceptual cross-section of a return capsule with an ablative heat shield. The heat shield and insulation limit heat transfer to the interior; layer arrangements and thicknesses depend on the materials and mission conditions." alt="A return capsule facing hypersonic flow, with its bow shock, heated gas layer, ablative heat shield, insulation, and internal payload identified." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-sun" %}{{ site.data.research-topics.applications[2].en.title }} {#solar-sail}

Solar sails generate thrust from solar radiation pressure as sunlight transfers momentum to the sail. We study how changing a sail's orientation alters its trajectory, and use this principle to design long-duration flights and future deep-space missions with reduced propellant needs.

- Astrodynamics accounting for solar radiation pressure and sail attitude
- Solar sail orbit raising and long-duration low-thrust trajectory design
- Non-Keplerian and other special orbits and future exploration mission concepts
- Solar sail in-space demonstration mission planning

{% include research-figure.html topic="solar-sail" caption="Sunlight transfers momentum to a sail, producing thrust. The right panel shows an ideal, perfectly reflecting sail in cross-section; sail orientation affects the magnitude and direction of thrust." alt="A deployed solar sail and a cross-section of an ideal reflective sail, showing incident and reflected light and thrust normal to the sail surface." %}

#### Solar Sail Deployment Mechanism: Development and Ground Tests {#solar-sail-ground-test}

The Korea Aerospace Research Institute (KARI) developed a ground test model with a 10 m × 10 m (100 m²) sail to advance solar sail deployment technology for deep-space exploration. A motor extends four supporting booms to unfurl the stowed membrane. Ground tests identified deployment problems and opportunities for improvement. The videos show the test model deploying from overhead and side views.

Further reading: [KARI press release (Korean)](https://www.kari.re.kr/kor/article/ATCL87374b48c/18228) · [Tests and Lessons Learned of Solar Sail Deployment](https://doi.org/10.52912/jsta.2026.6.3.293)

<div class="research-video-grid">
{% include research-video.html id="sail-test-overhead" file="kari-solar-sail-deployment-overhead.mp4" poster="kari-solar-sail-deployment-overhead.jpg" title="Solar sail deployment · overhead view (23 s clip)" %}
{% include research-video.html id="sail-test-side" file="kari-solar-sail-deployment-side.mp4" poster="kari-solar-sail-deployment-side.jpg" title="Solar sail deployment · side view (22 s clip)" %}
</div>

#### Deorbiter for Space Debris Removal: Development and Ground Tests {#deorbiter-ground-test}

KARI developed a ground test model of a deorbiter to investigate technologies for capturing and removing debris from low Earth orbit. It combines towing, capture, and deployment mechanisms. The concept uses a 5 m × 5 m (25 m²) drag sail to increase atmospheric drag and bring captured objects toward re-entry. The videos show ground tests of the drag-sail deployment function.

Further reading: [KARI press release (Korean)](https://www.kari.re.kr/kor/article/ATCL87374b48c/18417) · [Deorbiter development and tests](https://doi.org/10.52912/jsta.2026.6.2.196)

<div class="research-video-grid">
{% include research-video.html id="deorbiter-test-wide" file="kari-deorbiter-drag-sail-wide.mp4" poster="kari-deorbiter-drag-sail-wide.jpg" title="Drag-sail deployment · wide view (2.4 s clip)" %}
{% include research-video.html id="deorbiter-test-overhead" file="kari-deorbiter-drag-sail-overhead.mp4" poster="kari-deorbiter-drag-sail-overhead.jpg" title="Drag-sail deployment · overhead view (12.9 s clip)" %}
</div>

{% include section.html %}

### {% include icon.html icon="fa-solid fa-satellite-dish" %}{{ site.data.research-topics.applications[3].en.title }} {#optical-communications}

Deep-space optical communications uses lasers to exchange data between spacecraft and Earth. Our interests focus on how trajectories, spacecraft attitude, distance from Earth, and ground station weather and atmospheric conditions affect link performance. We aim to evaluate contact opportunities and data return, and to develop system requirements, operations plans, and technology demonstration scenarios within mass, power, and thermal limits.

- Link budgets and data transmission performance under range, optics, power, and loss constraints
- Pointing, acquisition, and tracking (PAT) requirements and spacecraft attitude stability
- Ground station placement and link availability under atmospheric, weather, and visibility constraints
- Combined radio-frequency (RF) and optical operations, transmission scheduling, and technology demonstration scenarios

{% include research-figure.html topic="optical-communications" caption="A conceptual laser downlink from a spacecraft to a ground telescope. Distance, pointing error, atmospheric conditions, and contact time affect data transmission performance." alt="A laser downlink from a spacecraft terminal through the atmosphere to a ground telescope, showing range, beam spread, pointing loss, power and optics, weather and link availability, and contact time and data return." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-satellite" %}{{ site.data.research-topics.applications[4].en.title }} {#cubesat}

We study how CubeSats can demonstrate mission concepts and technologies in space. Our interests span mission design, system requirements, ground testing, and in-orbit operations. Students may take part in these activities depending on the research project and its development schedule.

- CubeSat-class mission concepts and system requirements definition
- Ground testing and qualification methods for the space environment
- Satellite concepts of operations and in-orbit technology verification scenarios
- In-orbit demonstration mission planning linked to national R&D programs

{% include research-figure.html topic="cubesat" caption="CubeSat development translates a mission concept into system requirements, progresses through design, fabrication, and ground testing, and verifies technologies during in-orbit operations." alt="A conceptual CubeSat development and verification sequence from mission concept through system design, fabrication, ground testing, and in-orbit operations and demonstration." %}
