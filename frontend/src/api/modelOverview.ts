export interface modelDescript {
  modelName: string;
  modelType: string;
  modelEngine: string;
  descript: string;
  algorithm: string;
}

// 测试模型post的数据类型
export interface modelTestInfo{
    result: JSON;
    stdout: Array<string>;
    stderr: Array<string>;
}
export interface modelVariable {
  inputVariables: Array<JSON>;
  outputVariables: Array<JSON>;
}

export interface DatasetInfo {
  name: string;
  type: string;
  size: number;
  source: string;
  create_time: string;
}

export interface DatasetList {
  datasetList: Array<DatasetInfo>;
}

export interface PredictScript {
  code: string;
}

export interface userVarialbeValue {
  name: string;
  value: number;
}

