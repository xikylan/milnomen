import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import SpanishPage from "./components/SpanishPage";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <HomePage />
        </Route>
        <Route path="/es">
          <SpanishPage />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
