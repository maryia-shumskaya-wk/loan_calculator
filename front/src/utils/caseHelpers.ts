import _ from 'lodash';

export function objectToCamelCase(object: Object) {
    return Object.fromEntries(
        Object.entries(object).map(([key, item]) => (
            [_.camelCase(key), item]
        ))
    );
}

export function objectToSnakeCase(object: Object) {
    return Object.fromEntries(
        Object.entries(object).map(([key, item]) => (
            [_.snakeCase(key), item]
        ))
    );
}