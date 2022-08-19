export interface modelDescript {
    modelName: string;
    modelType: string;
    modelEngine: string;
    createTime : string;
    descript: string;
    algorithm: string;
  }

export interface jobResponseData {
    jobName: string;
    url: string;
    createTime: string;
    environment: string;
    dispatch: string;
    runList: Array<JSON>;
}

export interface testResponseData {
  args: string;
  env: Array<string>;
  jobName: string;
  runID: string;
  runName: string;
  scheduled: boolean;
  status: string;
}