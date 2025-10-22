// IST Format Patch - Inject this into the frontend
(function() {
  // Override formatDate function globally
  if (typeof window !== 'undefined') {
    window.formatDate = function(date) {
      if (!date) return 'Never'
      
      const dt = new Date(date)
      
      // Convert to IST (UTC + 5:30 hours)
      const istTime = new Date(dt.getTime() + (5.5 * 60 * 60 * 1000))
      
      // Format in Indian style: DD/MM/YYYY, H:MM:SS AM/PM IST
      const day = istTime.getUTCDate().toString().padStart(2, '0')
      const month = (istTime.getUTCMonth() + 1).toString().padStart(2, '0')
      const year = istTime.getUTCFullYear()
      const hours = istTime.getUTCHours()
      const minutes = istTime.getUTCMinutes().toString().padStart(2, '0')
      const seconds = istTime.getUTCSeconds().toString().padStart(2, '0')
      const ampm = hours >= 12 ? 'PM' : 'AM'
      const displayHours = hours % 12 || 12
      
      return `${day}/${month}/${year}, ${displayHours}:${minutes}:${seconds} ${ampm} IST`
    }
    
    console.log('IST formatDate function injected successfully!')
  }
})()
