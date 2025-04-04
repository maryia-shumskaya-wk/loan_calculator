import axios from 'axios';
import { objectToCamelCase, objectToSnakeCase } from '@/utils/caseHelpers';

const instance = axios.create({
    baseURL: 'http://localhost:8000/api',
});

// Used for cast request camelCase to snake_case
instance.interceptors.request.use((config) => {
    const data = config.data;
    if (!data) {
        return config;
    }
    config.data = objectToSnakeCase(data);
    return config;
});

// Used for cast response snake_case to camelCase
instance.interceptors.response.use((config) => {
    const data = config.data;
    if (!data) {
        return config;
    }
    let newData = null;
    if (Array.isArray(data)) {
        newData = data.map(item => objectToCamelCase(item));
    } else {
        newData = objectToCamelCase(data);
    }
    config.data = newData;
    return config;
});

type GetConfig = {
    additionalPath: string,
};

type DeleteConfig = {
    additionalPath: string,
}

type PutConfig = {
    additionalPath: string,
    data: any,
}

type PatchConfig = {
    additionalPath: string,
    data: any,
}

type PostConfig = {
    additionalPath: string,
    data: any,
}

interface IAPIClient {
    get(config: GetConfig) : Promise<any>
    put(config: PutConfig): Promise<any>
    patch(config: PatchConfig): Promise<any>
    delete(config: DeleteConfig): Promise<any>
    post(config: PostConfig): Promise<any>

}

class APIClient implements IAPIClient {

    get = ({
        additionalPath = "",
    }: GetConfig) => {
        return instance.get(`${additionalPath}`)
    }

    put = ({
        data,
        additionalPath = "",
    }: PutConfig) => {
        return instance.put(`${additionalPath}`, data)
    }

    patch = ({
        data,
        additionalPath = "",
    }: PatchConfig) => {
        return instance.patch(`${additionalPath}`, data)
    }

    delete = ({
        additionalPath = "",
    }: DeleteConfig) => {
        return instance.delete(`${additionalPath}`)
    }

    post = ({
        data,
        additionalPath = "",
    }: PostConfig) => {
        return instance.post(`${additionalPath}`, data)
    }
}

export default new APIClient();