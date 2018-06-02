// @flow
import React, { Component } from 'react'
import { ApolloClient } from 'apollo-client'
import { ApolloProvider } from 'react-apollo'
import { HttpLink } from 'apollo-link-http'
import { InMemoryCache } from 'apollo-cache-inmemory'
import { setContext } from 'apollo-link-context'

import { Provider } from 'react-redux'

import Routes from './Routes'
import configureStore from './redux/store'
import { AUTH_TOKEN } from './constants'

const httpLink = new HttpLink({
    uri: 'http://localhost:8080/api/graphql'
})

const authLink = setContext((_, { headers }) => {
    const token = localStorage.getItem(AUTH_TOKEN);
    console.log('token::::: ', token);
    
    // return the headers to the context so httpLink can read them
    return {
        headers: {
          ...headers,
          authorization: token ? `Bearer ${token}` : "",
        }
    }
})

const client = new ApolloClient({
    link: authLink.concat(httpLink),
    cache: new InMemoryCache()
})

const store = configureStore();

class App extends Component<{}>{
    
    render() {
        return (
            <Provider store={store}>
                <ApolloProvider client={client}>
                    <Routes />
                </ApolloProvider>
            </Provider>
        );
    }
}

export default App;
