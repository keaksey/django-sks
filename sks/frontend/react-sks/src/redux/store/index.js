// @flow
import { 
    createStore, 
    // applyMiddleware,
    // compose 
} from 'redux'

import rootReducer from './../reducers'

export default function configureStore(initialState: any ={}):any {
    let store = createStore(rootReducer, initialState);
    return store
}
