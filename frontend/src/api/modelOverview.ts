export interface modelDescript {
  modelName: string;
  modelType: string;
  modelEngine: string;
  descript: string;
  algorithm: string;
}

export interface modelVariable {
  inputVariables: Array<JSON>;
  outputVariables: Array<JSON>;
}
