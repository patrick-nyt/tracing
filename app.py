from random import randint
from flask import Flask, request
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

resource = Resource(attributes={
    SERVICE_NAME: "rolldice"
})

#jaeger_exporter = JaegerExporter(
#    agent_host_name="localhost",
#    agent_port=6831,
#)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
#processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
metrics.set_meter_provider(provider)
meter = metrics.get_meter(__name__)
roll_counter = meter.create_counter(
    "roll_counter",
    description="The number of rolls by roll value",
)

app = Flask(__name__)

@app.route("/rolldice")
def roll_dice():
    return str(do_roll())

def do_roll():
    with tracer.start_as_current_span("do_roll") as rollspan:  
        res = randint(1, 6)
        rollspan.set_attribute("roll.value", res)
        roll_counter.add(1, {"roll.value": res})
        return res


