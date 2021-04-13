import React from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import WordsPage from "./components/WordsPage";
import LearnPage from "./components/LearnPage";

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/">
          <HomePage />
        </Route>
        <Route path="/es/learn">
          <LearnPage srcLang="spanish" destLang="english" />
        </Route>
        <Route path="/es">
          <WordsPage srcLang="spanish" destLang="english" />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
