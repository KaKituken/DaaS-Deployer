export interface modelDescript {
  modelName: string;
  modelType: string;
  modelEngine: string;
  createTime: string;
  descript: string;
  algorithm: string;
}

export interface requireDataResponse {
  result: JSON;
  stdout: Array<string>;
  stderr: Array<string>;
}

/* 获取副本数据 */
export interface copyResponseData {
  restfulUrl: string;
  modelName: string;
  function: string;
  acessTimes: number;
  averageResponseTime: number;
  minResponseTime: number;
  maxResponseTime: number;
  firstAccessTime: string;
  lastAccessTime: string;
  createTime: string;
  serviceVersion: string;
  cpuReserve: string;
  memoryReserve: string;
  podList: Array<JSON>;
}

export const Sleep = (ms: any) => {
  return new Promise((resolve) => setTimeout(resolve, ms));
};
