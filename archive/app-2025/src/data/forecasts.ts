export interface Forecast {
  variable: string;
  cutoff_year: number;
  target_year: number;
  predicted: number;
  actual: number;
  lower: number;
  upper: number;
  model: string;
}

export const baselineForecasts: Forecast[] = [
  { variable: "HOMOSEX", cutoff_year: 1990, target_year: 2000, predicted: 14.6, actual: 27, lower: 8.8, upper: 20.4, model: "linear" },
  { variable: "HOMOSEX", cutoff_year: 1990, target_year: 2010, predicted: 15.6, actual: 41, lower: 6.9, upper: 24.4, model: "linear" },
  { variable: "HOMOSEX", cutoff_year: 1990, target_year: 2018, predicted: 16.5, actual: 58, lower: 5.4, upper: 27.5, model: "linear" },
  { variable: "HOMOSEX", cutoff_year: 1990, target_year: 2021, predicted: 16.8, actual: 64, lower: 4.9, upper: 28.7, model: "linear" },
  { variable: "HOMOSEX", cutoff_year: 2000, target_year: 2010, predicted: 29.0, actual: 41, lower: 13.7, upper: 44.3, model: "linear" },
  { variable: "HOMOSEX", cutoff_year: 2000, target_year: 2018, predicted: 33.2, actual: 58, lower: 11.8, upper: 54.7, model: "linear" },
  { variable: "HOMOSEX", cutoff_year: 2000, target_year: 2021, predicted: 34.8, actual: 64, lower: 11.0, upper: 58.6, model: "linear" },
  { variable: "GRASS", cutoff_year: 1990, target_year: 2000, predicted: 15.7, actual: 31, lower: 0, upper: 35.0, model: "linear" },
  { variable: "GRASS", cutoff_year: 1990, target_year: 2010, predicted: 13.4, actual: 44, lower: 0, upper: 42.4, model: "linear" },
  { variable: "GRASS", cutoff_year: 1990, target_year: 2018, predicted: 11.6, actual: 61, lower: 0, upper: 48.4, model: "linear" },
  { variable: "GRASS", cutoff_year: 1990, target_year: 2021, predicted: 11.0, actual: 68, lower: 0, upper: 50.6, model: "linear" },
  { variable: "GRASS", cutoff_year: 2000, target_year: 2010, predicted: 30.0, actual: 44, lower: 7.2, upper: 52.7, model: "linear" },
  { variable: "GRASS", cutoff_year: 2000, target_year: 2018, predicted: 32.3, actual: 61, lower: 0.4, upper: 64.2, model: "linear" },
  { variable: "GRASS", cutoff_year: 2000, target_year: 2021, predicted: 33.2, actual: 68, lower: 0, upper: 68.5, model: "linear" },
];

export const llmForecasts: Forecast[] = [
  { variable: "HOMOSEX", cutoff_year: 1990, target_year: 2000, predicted: 18, actual: 27, lower: 12, upper: 25, model: "claude" },
  { variable: "HOMOSEX", cutoff_year: 1990, target_year: 2010, predicted: 28, actual: 41, lower: 18, upper: 40, model: "claude" },
  { variable: "HOMOSEX", cutoff_year: 1990, target_year: 2018, predicted: 42, actual: 58, lower: 28, upper: 58, model: "claude" },
  { variable: "HOMOSEX", cutoff_year: 1990, target_year: 2021, predicted: 48, actual: 64, lower: 32, upper: 65, model: "claude" },
  { variable: "HOMOSEX", cutoff_year: 2000, target_year: 2010, predicted: 42, actual: 41, lower: 35, upper: 50, model: "claude" },
  { variable: "HOMOSEX", cutoff_year: 2000, target_year: 2018, predicted: 55, actual: 58, lower: 45, upper: 65, model: "claude" },
  { variable: "HOMOSEX", cutoff_year: 2000, target_year: 2021, predicted: 60, actual: 64, lower: 50, upper: 70, model: "claude" },
  { variable: "GRASS", cutoff_year: 1990, target_year: 2000, predicted: 22, actual: 31, lower: 18, upper: 28, model: "claude" },
  { variable: "GRASS", cutoff_year: 1990, target_year: 2010, predicted: 28, actual: 44, lower: 22, upper: 35, model: "claude" },
  { variable: "GRASS", cutoff_year: 1990, target_year: 2018, predicted: 35, actual: 61, lower: 28, upper: 43, model: "claude" },
  { variable: "GRASS", cutoff_year: 1990, target_year: 2021, predicted: 38, actual: 68, lower: 30, upper: 47, model: "claude" },
  { variable: "GRASS", cutoff_year: 2000, target_year: 2010, predicted: 42, actual: 44, lower: 35, upper: 50, model: "claude" },
  { variable: "GRASS", cutoff_year: 2000, target_year: 2018, predicted: 48, actual: 61, lower: 38, upper: 58, model: "claude" },
  { variable: "GRASS", cutoff_year: 2000, target_year: 2021, predicted: 51, actual: 68, lower: 40, upper: 62, model: "claude" },
];

export const historicalData = {
  HOMOSEX: {
    name: "Same-sex relations acceptance",
    question: "What about sexual relations between two adults of the same sex?",
    data: [
      { year: 1973, value: 11 },
      { year: 1980, value: 14 },
      { year: 1990, value: 13 },
      { year: 2000, value: 27 },
      { year: 2010, value: 41 },
      { year: 2018, value: 58 },
      { year: 2021, value: 64 },
    ],
  },
  GRASS: {
    name: "Marijuana legalization",
    question: "Do you think the use of marijuana should be made legal or not?",
    data: [
      { year: 1973, value: 19 },
      { year: 1980, value: 25 },
      { year: 1990, value: 16 },
      { year: 2000, value: 31 },
      { year: 2010, value: 44 },
      { year: 2018, value: 61 },
      { year: 2021, value: 68 },
    ],
  },
};

export const distributionData = {
  HOMOSEX: {
    2010: {
      actual: {
        "Always wrong": 44,
        "Not wrong at all": 41,
        "Sometimes wrong": 9,
        "Almost always wrong": 4,
      },
      llm: {
        "Always wrong": { estimate: 42, lower: 38, upper: 46 },
        "Not wrong at all": { estimate: 38, lower: 34, upper: 42 },
        "Sometimes wrong": { estimate: 12, lower: 9, upper: 15 },
        "Almost always wrong": { estimate: 5, lower: 3, upper: 7 },
      },
    },
  },
};

export const metrics = {
  baseline: { mae: 30.2, coverage: 35.7, bias: -30.2 },
  llm: { mae: 12.5, coverage: 42.9, bias: -12.4 },
  naive: { mae: 31.4, coverage: 7.1, bias: -31.4 },
  arima: { mae: 31.4, coverage: 50.0, bias: -31.4 },
  ets: { mae: 28.1, coverage: 28.6, bias: -7.1 },
};
