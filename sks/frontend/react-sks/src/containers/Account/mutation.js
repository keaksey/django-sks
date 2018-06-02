import gql from 'graphql-tag'

export const LOGIN_MUTATION = gql`
    mutation TokenCreate($username: String!, $password: String!) {
        tokenCreate(username: $username, password: $password) {
            token,
            errors {
                field
                message
            }
        }
    }
`
