#!/usr/bin/env python3
import re

# Read the file
with open('Client.vue', 'r') as f:
    content = f.read()

# Replace the device-counts fetch with API service call
old_pattern = r'const deviceCountsResponse = await fetch\("/api/clients/device-counts", \{\s*headers: \{ "Authorization": `Bearer \$\{localStorage\.getItem\("admin_token"\)\}` \s*\}\s*\}\)\.then\(r => r\.json\(\)\)'
new_pattern = 'const deviceCountsResponse = await apiService.getClientDeviceCounts()'

content = re.sub(old_pattern, new_pattern, content, flags=re.DOTALL)

# Write back to file
with open('Client.vue', 'w') as f:
    f.write(content)

print("Fixed device-counts API call")
