package lesson.outside;

import lesson.registration.Trace;
import org.springframework.stereotype.Component;

/** Annotated but intentionally outside ScanConfig's lesson.scan package. */
@Component
public final class Outside {
    public Outside() { Trace.outsiders++; Trace.record("Outside created"); }
}
