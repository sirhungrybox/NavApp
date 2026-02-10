export function formatCoordinate(value, type) {
  if (value === null || value === undefined) return '';

  const absValue = Math.abs(value);
  const degrees = Math.floor(absValue);
  const minutesFloat = (absValue - degrees) * 60;
  const minutes = Math.floor(minutesFloat);
  const seconds = ((minutesFloat - minutes) * 60).toFixed(1);

  let direction = '';
  if (type === 'lat') {
    direction = value >= 0 ? 'N' : 'S';
  } else {
    direction = value >= 0 ? 'E' : 'W';
  }

  return `${degrees}° ${minutes}' ${seconds}" ${direction}`;
}

export function parseCoordinate(input) {
  if (!input || input.trim() === '') return null;

  const trimmed = input.trim();

  // Try decimal degrees first
  const decimal = parseFloat(trimmed);
  if (!isNaN(decimal)) {
    return decimal;
  }

  // Try DMS format: 25° 16' 37.2" N
  const dmsRegex = /(-?)(\d+)[°\s]+(\d+)['\s]+(\d+\.?\d*)["\s]*([NSEW])?/i;
  const dmsMatch = trimmed.match(dmsRegex);
  if (dmsMatch) {
    const sign = dmsMatch[1] === '-' ? -1 : 1;
    const degrees = parseInt(dmsMatch[2]);
    const minutes = parseInt(dmsMatch[3]);
    const seconds = parseFloat(dmsMatch[4]);
    const direction = dmsMatch[5]?.toUpperCase();

    let result = sign * (degrees + minutes / 60 + seconds / 3600);
    if (direction === 'S' || direction === 'W') {
      result = -Math.abs(result);
    }
    return result;
  }

  // Try DDM format: 25° 16.620' N
  const ddmRegex = /(-?)(\d+)[°\s]+(\d+\.?\d*)['\s]*([NSEW])?/i;
  const ddmMatch = trimmed.match(ddmRegex);
  if (ddmMatch) {
    const sign = ddmMatch[1] === '-' ? -1 : 1;
    const degrees = parseInt(ddmMatch[2]);
    const minutes = parseFloat(ddmMatch[3]);
    const direction = ddmMatch[4]?.toUpperCase();

    let result = sign * (degrees + minutes / 60);
    if (direction === 'S' || direction === 'W') {
      result = -Math.abs(result);
    }
    return result;
  }

  return null;
}

export function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    weekday: 'short',
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

export function getMoonEmoji(phase) {
  const phases = {
    'New Moon': '🌑',
    'Waxing Crescent': '🌒',
    'First Quarter': '🌓',
    'Waxing Gibbous': '🌔',
    'Full Moon': '🌕',
    'Waning Gibbous': '🌖',
    'Last Quarter': '🌗',
    'Waning Crescent': '🌘'
  };
  return phases[phase] || '🌙';
}
