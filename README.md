# refinery-lf-exec-env [![Build Status](https://drone.dev.onetask.ai/api/badges/code-kern-ai/refinery-lf-exec-env/status.svg)](https://drone.dev.onetask.ai/code-kern-ai/refinery-lf-exec-env)
[![refinery repository](https://uploads-ssl.webflow.com/61e47fafb12bd56b40022a49/62c2f30f935f4d37dc864eeb_Kern%20refinery.png)](https://github.com/code-kern-ai/refinery)

Execution environment for labeling functions in [refinery](https://github.com/code-kern-ai/refinery). Containerized function as a service to execute user-defined Python scripts.

For classification tasks, the schema is
```python
from typing import Dict, Any

def my_labeling_function(record: Dict[str: Any]) -> str:
  return "my_label"
```

For extraction tasks, the schema is
```python
from typing import Dict, Any, Tuple

def my_labeling_function(record: Dict[str: Any]) -> Tuple[str, int, int]:
  start_idx = ...
  end_idx = ... # excluding format
  return "my_label", start_idx, end_idx
```

If you like what we're working on, please leave a ⭐ for [refinery](https://github.com/code-kern-ai/refinery)!
