import React from 'react'

import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

import Loadable from 'react-loadable'
import { LoadingPage, NotFound404 } from './components'

const AsyncAppMainPage = Loadable({
    loader: () => import("./containers"),
    loading: () => <LoadingPage />
})

export default function Routes() {
    
    return (
        <Router>
            <Switch>
                <Route path="/" component={AsyncAppMainPage}/>
                <Route component={NotFound404} />
            </Switch>
        </Router>
    )
}
