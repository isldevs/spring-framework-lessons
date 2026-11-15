# Constructor Injection in Spring Boot

Original English narration for iSLDevs. Seven coherent scene utterances. The local male Kokoro style targets a younger-to-middle adult explaining smoothly and conversationally. Actual source timing and model inference speed are recorded in source/timing.json; perceptual acceptance requires a listening review rather than only numeric checks.

1. How does an order service get its payment gateway?

2. Require a payment gateway in the constructor, and keep its reference in a final field.

3. Boot scans the components. One gateway bean matches that interface type.

4. Spring passes it into the service constructor before the application places an order.

5. Our Boot test confirms the same bean. A fake gateway passes a separate service test.

6. Require, resolve, inject, then use. Constructor injection makes required dependencies explicit.

7. Thanks for watching.

## Delivery and technical notes

- PaymentGateway is an interface; DemoGateway is the matching Spring-managed implementation. Do not depict an interface as an instantiated object.
- OrderService has one constructor accepting PaymentGateway and stores that reference in a final field. A final reference cannot be reassigned; it does not imply that the gateway object is immutable.
- @SpringBootApplication on CheckoutApplication starts the real Boot example and enables scanning from its application package. Do not imply that arbitrary packages are discovered automatically.
- This example has one matching gateway bean. Multiple candidates can need disambiguation. The single constructor does not need an @Autowired annotation.
- Spring supplies the managed gateway reference during service construction before application use. The OrderService does not construct its own gateway.
- The Boot integration check and the recording-fake service check are distinct: the latter manually supplies a fake through the constructor and does not register it as another production gateway bean.
- All approvals use a local simulated gateway. No real payment, card charge, external payment API or financial transaction occurs.
- Build the whole mechanism overview, hold the complete diagram for two seconds, then show and speak Thanks for watching. Do not speak internal scene labels or schedule identifiers.
- Public output contains no day, week, lesson or episode numbering.
