const fs = require('fs');

// Read the Client.vue file
let content = fs.readFileSync('./frontend/admin/src/views/Client.vue', 'utf8');

// Find the existing formatDate function and replace it
const oldFormatDate = `const formatDate = (timestamp) => {
      if (!timestamp) return 'N/A'
      const date = new Date(timestamp)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }`

const newFormatDate = `const formatDate = (timestamp) => {
      if (!timestamp) return 'N/A'
      
      // Parse as UTC timestamp (add Z if not present)
      const utcDate = new Date(timestamp.endsWith('Z') ? timestamp : timestamp + 'Z')
      
      // Convert to IST (UTC + 5:30 hours)
      const istTime = new Date(utcDate.getTime() + (5.5 * 60 * 60 * 1000))
      
      // Format in Indian style: DD/MM/YYYY, H:MM:SS AM/PM
      const day = istTime.getUTCDate().toString().padStart(2, '0')
      const month = (istTime.getUTCMonth() + 1).toString().padStart(2, '0')
      const year = istTime.getUTCFullYear()
      const hours = istTime.getUTCHours()
      const minutes = istTime.getUTCMinutes().toString().padStart(2, '0')
      const seconds = istTime.getUTCSeconds().toString().padStart(2, '0')
      const ampm = hours >= 12 ? 'PM' : 'AM'
      const displayHours = hours % 12 || 12
      
      return \`\${day}/\${month}/\${year}, \${displayHours}:\${minutes}:\${seconds} \${ampm}\`
    }`

// Replace the formatDate function
content = content.replace(oldFormatDate, newFormatDate)

// Write back
fs.writeFileSync('./frontend/admin/src/views/Client.vue', content)

console.log('✅ Successfully updated Client.vue formatDate function with IST format!')
