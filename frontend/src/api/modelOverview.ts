export interface modelDescript{
    modelName: string;
    modelType: string;
    modelEngine: string;
    descript: string;
    algorithm: string;
}

export interface modelVariable{
    inputVariables:Array<JSON>;
    outputVariables:Array<JSON>;
}

// 测试模型post的数据类型
export interface modelTestInfo{
    result: JSON;
    stdout: Array<string>;
    stderr: Array<string>;
}