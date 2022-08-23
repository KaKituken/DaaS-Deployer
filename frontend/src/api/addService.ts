export interface modelDeploy {
  version: Array<string>;
}

export interface addService {
  restfulUrl: string;
}

export interface status {
  status: boolean;
  detailed: string;
}
export interface settings {
  fileName: string;
  ext: string;
  jobName: string;
  jobDescription: string;
  serverVersion: string;
  variables: string;
  args: string;
  dispatch: string;
  runName: string;
}
