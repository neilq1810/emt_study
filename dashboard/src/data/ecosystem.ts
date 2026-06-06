// Curation layer for the data-driven explorers. Reference *details* live in the
// bibliography (single source of truth); this file holds only the curation —
// which work belongs to which research theme, the vendor relationship graph, and
// the corporate/product milestones that aren't bibliography entries. All facts
// trace to Chapters 2, 3, 28 and their cited sources.

export interface ThemeDef {
  desc: string;
  keys: string[]; // bibliography ids
}

// Academic-genealogy branches (Ch. 2 §2.4) + frontiers (Ch. 30).
export const themeMap: Record<string, ThemeDef> = {
  'Foundations & theory': {
    desc: 'The quasi-static magnetic-dipole formulation and its origins.',
    keys: ['raab1979', 'kuipers1975'],
  },
  'Excitation & decoding': {
    desc: 'Alternative excitations: rotating fields and transmitter arrays.',
    keys: ['paperno2001', 'plotkin2003'],
  },
  'Estimation & solvers': {
    desc: 'Recursive estimation, nonlinear least squares, and bounds.',
    keys: ['kalman1960', 'julier2004', 'barshalom2001', 'marquardt1963', 'kay1993', 'nocedal2006'],
  },
  'Medical validation & assessment': {
    desc: 'Standardized accuracy/distortion assessment of medical EMT.',
    keys: ['hummel2005', 'yaniv2009', 'franz2014', 'birkfellner1998', 'poulin2002'],
  },
  'Calibration & distortion compensation': {
    desc: 'Field mapping, polynomial/NN correction, witness-sensor methods.',
    keys: ['kindratenko2000', 'kindratenko2005', 'cavaliere2023'],
  },
  'Clinical applications': {
    desc: 'Electroanatomical mapping and navigation bronchoscopy outcomes.',
    keys: ['gepstein1997', 'folch2019'],
  },
  'Sensors & frontiers': {
    desc: 'Magnetic-sensor families, TMR noise, and quantum magnetometry.',
    keys: ['lenz2006', 'davies2021', 'monteblanco2021', 'budker2007', 'barry2020'],
  },
};

// Vendor relationship graph (Ch. 28; acquisitions are directed acquirer→target).
export interface VendorNode {
  id: string;
  label: string;
  kind: 'ac' | 'pulsed-dc' | 'medical-ep' | 'medical-nav' | 'holding';
  note: string;
  col: number; // layout column 0..3
  row: number; // layout row
}
export interface VendorEdge {
  from: string;
  to: string;
  label: string;
}

export const vendors: { nodes: VendorNode[]; edges: VendorEdge[] } = {
  nodes: [
    { id: 'polhemus', label: 'Polhemus', kind: 'ac', note: 'Founded 1969 (Bill Polhemus). AC tracking; FASTRAK/LIBERTY. Origin: military head-tracking.', col: 0, row: 0 },
    { id: 'ascension', label: 'Ascension', kind: 'pulsed-dc', note: 'Founded 1986 (Scully & Blood). Pulsed-DC; Flock of Birds / trakSTAR.', col: 0, row: 1 },
    { id: 'ndi', label: 'NDI', kind: 'medical-nav', note: 'Waterloo. Optical (Polaris) + EM (Aurora); OEM/research medical standard.', col: 1, row: 1 },
    { id: 'roper', label: 'Roper', kind: 'holding', note: 'Acquired NDI (2011); Ascension assets (2012).', col: 2, row: 1 },
    { id: 'biosense', label: 'Biosense', kind: 'medical-ep', note: 'Founded 1993 (Ben-Haim). Catheter localization; basis of CARTO.', col: 0, row: 2 },
    { id: 'jnj', label: 'Johnson & Johnson', kind: 'holding', note: 'Acquired Biosense (1997, ~$400M) → Biosense Webster; CARTO 3 (2009).', col: 2, row: 2 },
    { id: 'stjude', label: 'St. Jude → Abbott', kind: 'medical-ep', note: 'EnSite (impedance + magnetic). St. Jude acquired by Abbott (2017).', col: 0, row: 3 },
    { id: 'bsci', label: 'Boston Scientific', kind: 'medical-ep', note: 'Rhythmia (magnetic + impedance) EP mapping.', col: 0, row: 4 },
    { id: 'superdim', label: 'superDimension', kind: 'medical-nav', note: 'Electromagnetic navigation bronchoscopy (ENB).', col: 0, row: 5 },
    { id: 'covidien', label: 'Covidien', kind: 'holding', note: 'Acquired superDimension (2012, ~$300M).', col: 1, row: 5 },
    { id: 'medtronic', label: 'Medtronic', kind: 'holding', note: 'Closed Covidien acquisition (2015).', col: 2, row: 5 },
  ],
  edges: [
    { from: 'roper', to: 'ndi', label: 'acquired 2011' },
    { from: 'roper', to: 'ascension', label: 'acquired 2012' },
    { from: 'ndi', to: 'ascension', label: 'operates' },
    { from: 'jnj', to: 'biosense', label: 'acquired 1997' },
    { from: 'covidien', to: 'superdim', label: 'acquired 2012' },
    { from: 'medtronic', to: 'covidien', label: 'acquired 2015' },
  ],
};

// Milestones that are NOT bibliography entries (corporate/product events). Each
// cites a bibliography id for provenance (Ch. 3 §3.3 / Ch. 28).
export interface ExtraMilestone {
  year: number;
  label: string;
  kind: 'company' | 'product' | 'acquisition';
  ref: string;
}
export const extraMilestones: ExtraMilestone[] = [
  { year: 1969, label: 'Polhemus founded (AC tracking)', kind: 'company', ref: 'polhemus_history' },
  { year: 1986, label: 'Ascension founded (pulsed-DC)', kind: 'company', ref: 'ascension_roper2012' },
  { year: 1997, label: 'J&J acquires Biosense', kind: 'acquisition', ref: 'globes_jnj_biosense' },
  { year: 2000, label: 'NDI Aurora medical EMT (early 2000s)', kind: 'product', ref: 'ndi_history' },
  { year: 2009, label: 'CARTO 3 launched', kind: 'product', ref: 'globes_jnj_biosense' },
  { year: 2011, label: 'Roper acquires NDI', kind: 'acquisition', ref: 'ascension_roper2012' },
  { year: 2012, label: 'NDI acquires Ascension; Covidien acquires superDimension', kind: 'acquisition', ref: 'covidien_superdimension2012' },
  { year: 2015, label: 'Medtronic closes Covidien acquisition', kind: 'acquisition', ref: 'covidien_superdimension2012' },
];
