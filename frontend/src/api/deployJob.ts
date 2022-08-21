export interface modelDescript {
    modelName: string;
    modelType: string;
    modelEngine: string;
    createTime : string;
    descript: string;
    algorithm: string;
  }

export interface runListData {
    args: Array<JSON>
    createTime: string;
    duration: number;
    env: Array<JSON>;
    id: string;
    name: string;
    status: string;
  }

export interface jobResponseData {
    jobName: string;
    url: string;
    createTime: string;
    environment: string;
    dispatch: string;
    runList: Array<runListData>;
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