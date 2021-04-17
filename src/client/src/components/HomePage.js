import React from "react";
import { Container } from "react-bootstrap";
import NavigationBar from "./NavigationBar";
import JumboHeader from "./homepage/JumboHeader";
import LanguageList from "./homepage/LanguageList";

export default function HomePage() {
  return (
    <>
      <NavigationBar />
      <JumboHeader />
      <Container>
        <LanguageList />
      </Container>
    </>
  );
}
