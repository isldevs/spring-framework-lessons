package lesson.resolution;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import org.springframework.beans.TypeConverter;
import org.springframework.beans.factory.config.DependencyDescriptor;
import org.springframework.beans.factory.support.DefaultListableBeanFactory;

/** Observer-only subclass: all decisions and return values come from Spring. */
public final class TracingBeanFactory extends DefaultListableBeanFactory {
    public final List<String> events = new ArrayList<>();
    public List<String> compatibleNames = List.of();
    public List<String> eligibleNames = List.of();
    public final Map<String, Boolean> candidateDecisions = new LinkedHashMap<>();

    @Override
    public Object resolveDependency(DependencyDescriptor descriptor, String requestingBeanName,
            Set<String> autowiredBeanNames, TypeConverter typeConverter) {
        if (descriptor.getDependencyType() == PaymentGateway.class) {
            events.add("resolveDependency: PaymentGateway");
        }
        return super.resolveDependency(descriptor, requestingBeanName, autowiredBeanNames, typeConverter);
    }

    @Override
    protected Map<String, Object> findAutowireCandidates(String beanName, Class<?> requiredType,
            DependencyDescriptor descriptor) {
        boolean observed = requiredType == PaymentGateway.class;
        if (observed) {
            compatibleNames = List.copyOf(Arrays.asList(getBeanNamesForType(requiredType)));
            events.add("compatible types: " + compatibleNames);
        }
        Map<String, Object> result = super.findAutowireCandidates(beanName, requiredType, descriptor);
        if (observed) {
            eligibleNames = List.copyOf(result.keySet());
            events.add("eligible candidates: " + eligibleNames);
        }
        return result;
    }

    @Override
    public boolean isAutowireCandidate(String beanName, DependencyDescriptor descriptor) {
        boolean decision = super.isAutowireCandidate(beanName, descriptor);
        if (descriptor.getDependencyType() == PaymentGateway.class) {
            candidateDecisions.put(beanName, decision);
            events.add("isAutowireCandidate " + beanName + ": " + decision);
        }
        return decision;
    }
}
