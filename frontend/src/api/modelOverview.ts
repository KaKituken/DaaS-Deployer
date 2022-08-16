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

export interface DatasetInfo{
   name: string;
   type: string;
   size: number;
   source: string;
   create_time: string;
}

export interface DatasetList {
  datasetList: Array<DatasetInfo>;
}

export interface PredictScript{
  code: string;
}