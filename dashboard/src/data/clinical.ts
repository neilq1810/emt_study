// Clinical use-case scenarios (Ch. 29). Curated and sourced; every quantitative
// fact cites a bibliography id (joined to its URL in the page).

export interface Fact { label: string; value: string; ref?: string }
export interface Scenario {
  id: string;
  name: string;
  instrument: string;
  blurb: string;
  steps: string[];
  emtRole: string;
  facts: Fact[];
  dominantErrors: string[];
  refs: string[];
}

export const scenarios: Scenario[] = [
  {
    id: 'ep',
    name: 'Cardiac electrophysiology & ablation',
    instrument: 'catheter',
    blurb: 'Building a 3-D electroanatomical map of a heart chamber to guide ablation of arrhythmia substrate — without continuous fluoroscopy.',
    steps: [
      'Position a low-field generator (location pad) under the patient',
      'Navigate a magnetically-tracked catheter through the chamber',
      'Acquire geometry + local electrograms → color-coded activation map',
      'Target and ablate; re-map to confirm',
    ],
    emtRole: 'Drift-free, line-of-sight-free localization of the catheter tip inside the beating heart; often fused with impedance-based localization.',
    facts: [
      { label: 'Localization', value: 'Nonfluoroscopic, 6-DOF magnetic; in vitro/in vivo accuracy validated', ref: 'gepstein1997' },
      { label: 'Key benefit', value: 'Reduced ionizing-radiation dose to patient and staff', ref: 'gepstein1997' },
    ],
    dominantErrors: ['Cardiac/respiratory motion', 'Ferromagnetic instruments in field', 'Catheter–tip offset'],
    refs: ['gepstein1997', 'franz2014'],
  },
  {
    id: 'enb',
    name: 'Electromagnetic navigation bronchoscopy',
    instrument: 'bronchoscope',
    blurb: 'Reaching peripheral lung lesions beyond bronchoscopic vision using a CT-derived airway map and an EM-tracked steerable catheter.',
    steps: [
      'Plan a path on the pre-procedure CT (virtual bronchial tree)',
      'Register the patient to the CT',
      'Navigate the EM-tracked catheter to the lesion',
      'Biopsy under navigation',
    ],
    emtRole: 'Localizes the catheter tip within the airways where there is no line of sight, against the planning CT.',
    facts: [
      { label: '12-month diagnostic yield', value: '≈ 73% (NAVIGATE, >1000 subjects)', ref: 'folch2019' },
      { label: 'Pneumothorax (grade ≥2)', value: '≈ 2.9%', ref: 'folch2019' },
    ],
    dominantErrors: ['Respiratory motion (CT-to-body divergence)', 'Registration error', 'Airway deformation'],
    refs: ['folch2019', 'covidien_superdimension2012'],
  },
  {
    id: 'ent',
    name: 'ENT & skull-base navigation',
    instrument: 'pointer/probe',
    blurb: 'Localizing instruments relative to CT near critical structures (orbit, skull base, carotid) in the confined nasal corridor.',
    steps: [
      'Acquire and segment the pre-operative CT',
      'Register patient to CT (fiducials / surface)',
      'Track instruments without line-of-sight constraints',
      'Display tip position on the CT intra-operatively',
    ],
    emtRole: 'No-line-of-sight tracking in a corridor where the scope and hands block optical sightlines.',
    facts: [
      { label: 'Intra-op localization', value: '≈ 1–2 mm (application- and registration-dependent)', ref: 'franz2014' },
      { label: 'Dominant term', value: 'Registration error often exceeds tracker error', ref: 'yaniv2009' },
    ],
    dominantErrors: ['Patient-to-CT registration', 'Tissue shift', 'Nearby ferromagnetic instruments'],
    refs: ['franz2014', 'yaniv2009'],
  },
  {
    id: 'ir',
    name: 'Interventional radiology & biopsy',
    instrument: 'needle',
    blurb: 'Guiding needles/probes in percutaneous procedures, fused with CT or ultrasound, where the tip is inside the patient.',
    steps: [
      'Co-register tracking to the imaging volume (CT/US)',
      'Track the needle/probe tip in real time',
      'Display the tracked tool on pre-acquired or live imaging',
      'Advance to target',
    ],
    emtRole: 'Line-of-sight-free tip localization fused with imaging; the enabling property for in-body needles.',
    facts: [
      { label: 'Ambient EM noise error', value: '< 0.15 mm RMS even in an OR', ref: 'poulin2002' },
      { label: 'Ferromagnetic/electrical distorters', value: 'up to 8.4 mm / 166° if too close', ref: 'poulin2002' },
      { label: 'Dynamic compensation', value: 'C-arm distortion reduced to 1.52 mm RMS (witness sensor)', ref: 'cavaliere2023' },
    ],
    dominantErrors: ['CT gantry / C-arm distortion', 'Target motion', 'Registration'],
    refs: ['yaniv2009', 'poulin2002', 'cavaliere2023'],
  },
  {
    id: 'robotic',
    name: 'Robotic surgery & image-guided therapy',
    instrument: 'robotic catheter',
    blurb: 'Providing instrument pose to robotic and IGT platforms where optical tracking cannot see, fused with robot kinematics, IMU and imaging.',
    steps: [
      'Time-synchronize EM pose with robot kinematics / IMU / imaging',
      'Fuse modalities into a single timestamped pose + covariance',
      'Close the control / guidance loop on the fused estimate',
      'Flag and degrade gracefully under distortion',
    ],
    emtRole: 'Absolute, occlusion-robust pose that complements robot encoders and (occludable) optical tracking.',
    facts: [
      { label: 'Critical factors', value: 'Bounded latency, cross-modality time alignment, fault flagging', ref: 'franz2014' },
    ],
    dominantErrors: ['Latency / time-skew between modalities', 'Field distortion', 'Calibration of tool-to-sensor transform'],
    refs: ['franz2014'],
  },
];
