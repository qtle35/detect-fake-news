import React from 'react';
import { Container, Tab, Tabs } from 'react-bootstrap';

import ModelStatDetail from './model-stat-detail';

function ModelStatPage() {
  return (
    <Container>
      <h1>Model Statistic</h1>
      <Tabs
        defaultActiveKey="nbmodel"
        id="uncontrolled-tab-example"
        className="mb-3"
      >
        <Tab eventKey="nbmodel" title="Naive Bayes">
          <ModelStatDetail name="nbmodel" />
        </Tab>
        <Tab eventKey="lrmodel" title="Logistic Regression">
         <ModelStatDetail name="lrmodel" />
        </Tab>
        <Tab eventKey="pacmodel" title="Passive Aggressive Classifier">
          <ModelStatDetail name="pacmodel" />
        </Tab>
      </Tabs>

    </Container>
  );
}

export default ModelStatPage;