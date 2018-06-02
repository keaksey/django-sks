// @flow
import React from "react"
import { Route, Redirect } from "react-router-dom"

function querystring(name: string, url: string = window.location.href) {
    name = name.replace(/[[]]/g, "\\$&");
    const regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)", "i");
    const results = regex.exec(url);
    
    if (!results) {
        return null;
    }
    
    if (!results[2]) {
        return "";
    }
    
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

export function UnauthenticatedRoute({ component, props, ...rest }: any) {
  const redirect = querystring("redirect");
  const C = component;
  const cProps = props;
  
  return (
        <Route
          {...rest}
          render={(params: any) =>
            !cProps.isAuthenticated
              ? <C {...params} {...cProps} />
              : <Redirect
                  to={redirect === "" || redirect === null ? "/" : redirect}
                />
            }
        />
  );
}