// @flow
import React from 'react'

import {
  Route,
  Switch
} from 'react-router-dom'

import Loadable from 'react-loadable'
import { LoadingPage, NotFound404 } from './../components'
import { UnauthenticatedRoute } from './../components/Routes'

const AsyncAppLogin = Loadable({
    loader: () => import("./Account").then((c) => c.Login),
    loading: () => <LoadingPage />
})

const AsyncStoreFront = Loadable({
    loader: () => import("./StoreFront"),
    loading: () => <LoadingPage />
})

export default function Routes({ childProps }: any) {
    childProps = childProps || {isAuthenticated: false}
    
    return (
        <Switch>
            <UnauthenticatedRoute 
              exact path="/" 
              component={AsyncStoreFront}
              props={childProps}
            />
            <UnauthenticatedRoute 
              exact path="/account/login" 
              component={AsyncAppLogin}
              props={childProps}
            />
            <Route component={NotFound404} />
        </Switch>
    )
}
