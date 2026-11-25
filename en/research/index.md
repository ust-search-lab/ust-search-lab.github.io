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
  <a href="#entry-systems">Entry, descent, landing &amp; thermal protection</a>
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

We develop orbits and concepts of operations to meet mission objectives. We predict long-term orbital evolution under Earth's nonspherical gravity and atmospheric drag, and examine orbit maintenance strategies for the mission duration.

#### Satellite constellation design {#earth-constellation}

For Earth observation, communications, and technology demonstration, we design satellite count, orbital altitude and inclination, orbital planes, and phasing. We compare coverage, revisit intervals, and contact opportunities alongside propellant use and operational effort to identify suitable configurations.

For formation flying that requires precise relative positioning, we address [guidance and control](#guidance-control) using relative orbit dynamics and accounting for navigation errors.

{% include research-figure.html topic="earth-constellation" caption="Illustrative constellation with satellites distributed across three orbital planes. Colors distinguish the planes; satellite sizes and orbital altitudes are not to scale." alt="A schematic of satellites distributed across three circular orbits around Earth, with altitude, inclination, orbital planes, and satellite phasing identified as design variables." %}

#### Orbital datacenters {#orbital-datacenter}

We assess the feasibility of storing and processing data in space by integrating power, thermal management, and communications requirements. We compare candidate orbits and data processing and transfer plans against sunlight and eclipse periods and inter-satellite and ground contact opportunities.

{% include section.html %}

### {% include icon.html icon="fa-solid fa-moon" %}{% include research-title.html id="planetary" %} {#planetary}

We design lunar and planetary exploration missions, including lunar landers and Mars orbiters and landers.

- Conceptual design of lunar exploration and landing missions and Mars orbiter and lander missions
- Orbit and landing site assessment against exploration objectives
- Observation and communications geometry between spacecraft, surface targets, and Earth
- Spacecraft operations scenarios based on observation and contact opportunities

{% include research-figure.html image="mars-transfer-porkchop-trajectory.jpg" width="2600" height="1167" caption="Example of 2035 Earth–Mars transfer design. (a) Porkchop plot of launch energy (C3) by departure date and time of flight, with the Naro Space Center launch envelope. (b) Transfer trajectory departing in May 2035 and entering the Martian atmosphere in December, with trajectory correction maneuvers (TCMs)." alt="(a) Contours of launch energy C3 against 2035 departure date and time of flight, marking the baseline solution, the minimum-C3 alternative, the Naro Space Center launch envelope, and solutions meeting the entry-speed condition. (b) Heliocentric view of the Earth and Mars orbits and the 200-day transfer from Earth departure on May 26, 2035 to Mars entry on December 12, with four trajectory correction maneuvers." credit="KARI, KASA Space Challenge Program Mars EDL key technology project" %}

#### Dynamical systems and multi-body astrodynamics {#multi-body-dynamics}

We use dynamical structures of the three-body problem, such as Lagrange points, periodic orbits, and invariant manifolds, in trajectory design for lunar and planetary exploration.

{% include research-figure.html image="cr3bp-manifolds.png" width="2400" height="990" caption="Dynamical structure of the Earth–Moon circular restricted three-body problem. (a) The five Lagrange points (L1–L5) in the rotating frame and the forbidden region (gray) that a spacecraft cannot enter at the given energy. The large dot is the Earth and the small dot is the Moon. (b) Close-up near the Moon. Stable manifolds (blue) approaching the periodic orbits around L1 and L2 (black) and unstable manifolds (orange) departing from them form a passage from the Earth region through the Moon region to the exterior. Structures like these underpin low-energy transfer design." alt="(a) The Earth, the Moon, the Lagrange points L1 to L5, and a ring-shaped gray forbidden region in the Earth–Moon rotating frame, with a dashed box marking the close-up region near the Moon. (b) Close-up near the Moon showing black periodic orbits around L1 and L2, a blue tube entering the L1 orbit from the Earth side, an orange tube leaving the L1 orbit toward the Moon, a blue tube entering the L2 orbit from the Moon side, and an orange tube leaving the L2 orbit to the exterior." credit="SEARCH Lab" %}

##### Earth–Moon cycler orbits {#cycler}

A cycler is an orbit that travels back and forth between the Earth and the Moon, passing both bodies repeatedly. In an idealized model it repeats the round trip without propulsion, which makes it a candidate orbit for regular Earth–Moon transport and repeated observation.

SEARCH Lab is interested in whether cyclers that are stable in the idealized model can keep their repeated encounters in a realistic environment. Building on [dynamical systems and multi-body astrodynamics](#dynamical-systems), we study the following problems.

- Computation and stability analysis of periodic cycler orbits in the circular restricted three-body problem
- The effect of lunar orbital eccentricity and solar gravity on the persistence of repeated close passes
- How well stability in the idealized model predicts whether repeated encounters can be maintained in a realistic environment
- Design of orbits and correction maneuvers that maintain repeated encounters in realistic ephemeris models

{% include research-figure.html image="earth-moon-cyclers.png" width="2400" height="885" caption="Three periodic cycler orbits in the Earth–Moon rotating frame. The large dot is the Earth and the small dot is the Moon; distances are in units of the Earth–Moon distance. In the circular restricted three-body problem these orbits repeat the same path without propulsion; the families were reported in earlier work and recomputed independently here. The numbers in parentheses label the orbit family, and T is the period in days." alt="Three cycler orbits in the x–y plane of the Earth–Moon rotating frame. The (1,1) orbit, with a period of 44.8 days, encloses the Earth and makes a small loop around the Moon; the (3,1) orbit, 64.3 days, and the (3,3) orbit, 78.9 days, circle the Earth several times in a star-like pattern before passing near the Moon." credit="SEARCH Lab" %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-parachute-box" %}{% include research-title.html id="entry-systems" %} {#entry-systems}

#### Mars entry, descent, and landing {#edl}

SEARCH Lab studies entry, descent, and landing (EDL) technologies that allow a Mars spacecraft to enter the atmosphere, slow down, and land safely on the surface. We develop key technologies for each phase, from atmospheric entry through deceleration and landing, verify end-to-end performance through integrated simulation, and build the technical foundation for future Mars exploration.

- Entry trajectory analysis and simulation validation that account for the Martian atmospheric environment
- Spacecraft shape design and thermal protection technologies for atmospheric entry
- Guidance, control, and parachute deceleration technologies for stable descent
- Navigation, hazard avoidance, and landing control technologies for precise and safe landing
- Integrated simulation linking every phase from entry to landing, and mission performance analysis

{% include research-figure.html image="mars-edl-korean-lander-sequence.jpg" width="2058" height="1138" caption="EDL sequence for a Korean Mars landing mission concept, from atmospheric entry through parachute deployment, powered descent, and touchdown to atmospheric observations on the surface." alt="A labeled 15-step sequence: 01 entry interface point, 02 peak heating, 03 peak deceleration, 04 hypersonic guided flight, 05 parachute deployment, 06 heat shield separation with 06A release of ten free-fall probes, 07 landing leg deployment, 08 radar acquisition and TRN, 09 backshell separation and powered descent, 10 hazard avoidance, 11 vertical descent, 12 touchdown and engine cutoff, 13 balloon inflation, 14 balloon release, and 15 radiosonde science." credit="KARI, KASA Space Challenge Program Mars EDL key technology project" %}

<div class="research-video-grid research-video-grid--single">
{% include research-video.html id="mars-edl-korean-lander-conops" file="mars-edl-korean-lander-conops.mp4" poster="mars-edl-korean-lander-conops.jpg" title="Concept of operations for a Korean Mars landing mission, from atmospheric entry to surface operations (3× speed, 63 s; Korean labels)" %}
</div>

<p class="research-video-credit">Video: KARI</p>

##### Thermal protection materials for Mars atmospheric entry: development and testing {#mars-tps}

Compared with Earth re-entry, Mars entry involves lower entry speeds and heat fluxes, but heating lasts longer. For this environment, we develop lightweight, low-density ablative thermal protection materials that can be produced domestically.

On November 10, 2026, KARI, the Korea Institute of Ceramic Engineering and Technology (KICET), and DACC Carbon jointly tested thermal protection materials in the 300 kW-class arc-jet facility at Vitzro Nextech.

<div class="research-video-grid">
{% include research-video.html id="mars-tps-arcjet-flow" file="mars-tps-arcjet-flow.mp4" poster="mars-tps-arcjet-flow.jpg" title="Arc-jet plasma flow heating a specimen (32 s)" %}
{% include research-video.html id="mars-tps-arcjet-infrared" file="mars-tps-arcjet-infrared.mp4" poster="mars-tps-arcjet-infrared.jpg" title="Surface temperature measured with an infrared camera (21 s)" %}
{% include research-video.html id="mars-tps-arcjet-side" file="mars-tps-arcjet-side.mp4" poster="mars-tps-arcjet-side.jpg" title="Side view of a heated specimen (32 s)" %}
{% include research-video.html id="mars-tps-arcjet-front" file="mars-tps-arcjet-front.mp4" poster="mars-tps-arcjet-front.jpg" title="Surface of a heated specimen (32 s)" %}
</div>

<p class="research-video-credit">Videos: joint arc-jet test by KARI, KICET, and DACC Carbon (Vitzro Nextech, November 10, 2026)</p>

##### Parachute deceleration technology {#mars-parachute}

We study technologies for decelerating a spacecraft by deploying a parachute at supersonic speed in the thin Martian atmosphere. Yonsei University and KARI performed fluid-structure interaction analyses that resolve the canopy's structural response together with the surrounding flow during parachute deployment.

<div class="research-video-grid">
{% include research-video.html id="mars-parachute-canopy-stress" file="mars-parachute-canopy-stress.mp4" poster="mars-parachute-canopy-stress.jpg" title="Canopy stress (16 s)" %}
{% include research-video.html id="mars-parachute-flow-pressure" file="mars-parachute-flow-pressure.mp4" poster="mars-parachute-flow-pressure.jpg" title="Flow pressure (16 s)" %}
{% include research-video.html id="mars-parachute-flow-density" file="mars-parachute-flow-density.mp4" poster="mars-parachute-flow-density.jpg" title="Flow density (16 s)" %}
{% include research-video.html id="mars-parachute-flow-velocity-z" file="mars-parachute-flow-velocity-z.mp4" poster="mars-parachute-flow-velocity-z.jpg" title="Flow z-velocity (16 s)" %}
</div>

<p class="research-video-credit">Videos: Yonsei University and KARI, fluid-structure interaction analysis of a supersonic parachute</p>

#### Earth re-entry and thermal protection systems {#reentry}

We analyze aerodynamic heating and deceleration loads as spacecraft and sample return capsules enter Earth's atmosphere at high speed. We study how to design and verify heat shields and other thermal protection systems by considering re-entry trajectories and thermal environments together.

- Re-entry trajectories, entry corridors, and recovery scenarios for sample return capsules
- Prediction of re-entry environments, including aerodynamic heating and deceleration loads
- Thermal protection system concepts and thickness sizing, and thermal response analysis of ablative and reusable materials
- Verification methods using ground tests, such as arc-jet testing, and flight tests

{% include research-figure.html topic="reentry" caption="A conceptual cross-section of a sample-return capsule showing the detached bow shock, the hot shock layer, stagnation-point heating, and the forebody ablator and backshell thermal protection. The enlarged stack-up shows the temperature profile through the ablator and the bondline temperature limit that sizes its thickness. Shapes and thicknesses are not to scale." alt="A sample-return capsule facing hypersonic flow and a detached bow shock, with the stagnation point, forebody ablator, backshell thermal protection, structure, and sample canister identified. An enlarged stack-up shows the char, pyrolysis, and virgin ablator zones, the bondline, and the temperature profile, and a band below shows the analysis flow from entry trajectory to aerothermal environment, thermal protection sizing, and arc-jet and flight testing." %}

{% include section.html %}

### {% include icon.html icon="fa-solid fa-sun" %}{% include research-title.html id="solar-sail" %} {#solar-sail}

Solar sails generate thrust from solar radiation pressure as sunlight transfers momentum to the sail. We study how changing a sail's orientation alters its trajectory, and use this principle to design long-duration flights and future deep-space missions with reduced propellant needs.

- Astrodynamics accounting for solar radiation pressure and sail attitude
- Solar sail orbit raising and long-duration low-thrust trajectory design
- Non-Keplerian and other special orbits and future exploration mission concepts
- Solar sail in-space demonstration mission planning

#### Integrated attitude and orbit control {#integrated-attitude-orbit-control}

We combine [guidance and control](#optimization) with [attitude dynamics and control](#attitude-dynamics-control) to analyze and control coupled solar-sail orbit and attitude motion. We model solar radiation pressure forces and torques, including center-of-mass and center-of-pressure geometry, and assess mission feasibility through six-degree-of-freedom simulation with actuator limits and observation and communications pointing constraints. We also examine [AI and machine learning](#ai-machine-learning) for control command prediction and autonomous flight.

Related prior work: [Indirect methods for deep-learning-based solar-sail optimal control (2025, Korean)](https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12589746)

#### Solar sail deployment mechanism: development and ground tests {#solar-sail-ground-test}

The Korea Aerospace Research Institute (KARI) developed a ground test model with a 10 m × 10 m (100 m²) sail to advance solar sail deployment technology for deep-space exploration. A motor extends four supporting booms to unfurl the stowed membrane. Ground tests identified deployment problems and opportunities for improvement. The videos show the test model deploying from overhead and side views.

Further reading: [KARI press release (Korean)](https://www.kari.re.kr/kor/article/ATCL87374b48c/18228), [Tests and Lessons Learned of Solar Sail Deployment](https://doi.org/10.52912/jsta.2026.6.3.293)

<div class="research-video-grid">
{% include research-video.html id="sail-test-overhead" file="kari-solar-sail-deployment-overhead.mp4" poster="kari-solar-sail-deployment-overhead.jpg" title="Solar sail deployment, overhead view (23 s)" %}
{% include research-video.html id="sail-test-side" file="kari-solar-sail-deployment-side.mp4" poster="kari-solar-sail-deployment-side.jpg" title="Solar sail deployment, side view (22 s)" %}
</div>

#### Deorbiter for space debris removal: development and ground tests {#deorbiter-ground-test}

KARI developed a ground test model of a deorbiter to investigate technologies for capturing and removing debris from low Earth orbit. It combines towing, capture, and deployment mechanisms. The concept uses a 5 m × 5 m (25 m²) drag sail to increase atmospheric drag and bring captured objects toward re-entry. The videos show ground tests of the drag-sail deployment function.

Further reading: [KARI press release (Korean)](https://www.kari.re.kr/kor/article/ATCL87374b48c/18417), [Deorbiter development and tests](https://doi.org/10.52912/jsta.2026.6.2.196)

<div class="research-video-grid">
{% include research-video.html id="deorbiter-test-wide" file="kari-deorbiter-drag-sail-wide.mp4" poster="kari-deorbiter-drag-sail-wide.jpg" title="Drag-sail deployment, wide view (2.4 s)" %}
{% include research-video.html id="deorbiter-test-overhead" file="kari-deorbiter-drag-sail-overhead.mp4" poster="kari-deorbiter-drag-sail-overhead.jpg" title="Drag-sail deployment, overhead view (12.9 s)" %}
</div>

{% include section.html %}

### {% include icon.html icon="fa-solid fa-satellite-dish" %}{% include research-title.html id="optical-communications" %} {#optical-communications}

Deep-space optical communications uses lasers to exchange data between spacecraft and Earth. We study how trajectories, spacecraft attitude, distance from Earth, and ground station weather and atmospheric conditions affect link performance. We evaluate contact opportunities and data return, and develop system requirements, operations plans, and technology demonstration scenarios within mass, power, and thermal limits.

- Link budgets and data transmission performance under range, optics, power, and loss constraints
- Pointing, acquisition, and tracking (PAT) requirements and spacecraft attitude stability
- Ground station placement and link availability under atmospheric, weather, and visibility constraints
- Combined radio-frequency (RF) and optical operations, transmission scheduling, and technology demonstration scenarios

{% include research-figure.html topic="optical-communications" caption="A conceptual laser downlink from a spacecraft to a ground telescope. Distance, pointing error, atmospheric conditions, and contact time affect data transmission performance." alt="A laser downlink from a spacecraft terminal through the atmosphere to a ground telescope, showing range, beam spread, pointing loss, power and optics, weather and link availability, and contact time and data return." %}

#### Receiver-model analysis of Mars–Earth optical links {#mars-optical-downlink}

In a Mars–Earth optical downlink, very few photons arrive per pulse, so the statistical model chosen for the receiver can change the conclusions of the link budget. For a Mars–Earth downlink using M-ary pulse-position modulation (M-PPM), SEARCH Lab fixed the optical link conditions and compared an avalanche photodiode (APD) Gaussian model with an ideal Poisson photon-counting model. Under the same conditions, the required number of signal photons differed by a factor of 4.7–6.2 depending on the model, and the difference came from the detector noise model rather than the shape of the probability distribution. This factor is a sensitivity to the choice of model, not a performance difference between real detectors.

{% include research-figure.html image="mars-optical-receiver-models.png" width="2000" height="1428" caption="Uncoded bit-error rate versus signal photons per pulse. Solid lines are the APD Gaussian receiver model, dashed lines are the ideal Poisson photon-counting model, and M is the PPM order. The number of photons required for the same error rate depends on the receiver model." alt="A log-log plot of uncoded bit-error rate against signal photons per pulse. Three solid curves for the APD Gaussian model and three dashed curves for the ideal Poisson model are drawn for PPM orders 16, 64, and 256; the dashed curves fall at fewer photons than the solid ones." credit="Jae-ik Park, paper accepted in Optical and Quantum Electronics (2026)" %}

Related paper: Jae-ik Park, "Decomposing Receiver-Model Sensitivity in M-PPM Mars–Earth Optical Downlinks: APD Gaussian and Ideal Poisson Models," *Optical and Quantum Electronics*, accepted (2026). [Publications]({{ '/en/publications/' | relative_url }})

{% include section.html %}

### {% include icon.html icon="fa-solid fa-satellite" %}{% include research-title.html id="cubesat" %} {#cubesat}

We study how CubeSats can demonstrate mission concepts and technologies in space. Our interests span mission design, system requirements, ground testing, and in-orbit operations. Student researchers conduct research linked to relevant national R&D programs, with the scope of their involvement and responsibilities determined by research topics and project schedules.

- CubeSat-class mission concepts and system requirements definition
- Ground testing and qualification methods for the space environment
- Satellite concepts of operations and in-orbit technology verification scenarios
- In-space demonstration mission planning linked to national R&D programs

For [attitude control](#attitude-dynamics-control) and autonomous control algorithms, we consider verification from numerical simulation to ground tests integrating onboard computers, sensors, and actuators, and assess opportunities for in-orbit demonstration according to project scope and resources.

{% include research-figure.html topic="cubesat" caption="CubeSat development translates a mission concept into system requirements, progresses through design, fabrication, and ground testing, and verifies technologies during in-orbit operations." alt="A conceptual CubeSat development and verification sequence from mission concept through system design, fabrication, ground testing, and in-orbit operations and demonstration." %}
