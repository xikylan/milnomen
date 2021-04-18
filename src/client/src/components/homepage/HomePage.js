import React from "react";
import { Container } from "react-bootstrap";
import JumboHeader from "./JumboHeader";
import LanguageList from "./LanguageList";

export default function HomePage() {
  return (
    <>
      <JumboHeader />
      <Container>
        <LanguageList />
      </Container>
    </>
  );
}
