"""BoundingBox dataclass with intersection and expansion operations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BBox:
    """Bounding box in EPSG:4326 (WGS84).

    Attributes:
        west: Minimum longitude (degrees).
        south: Minimum latitude (degrees).
        east: Maximum longitude (degrees).
        north: Maximum latitude (degrees).
    """

    west: float
    south: float
    east: float
    north: float

    def __post_init__(self) -> None:
        """Validate bbox bounds."""
        if self.west >= self.east:
            msg = "west must be less than east"
            raise ValueError(msg)
        if self.south >= self.north:
            msg = "south must be less than north"
            raise ValueError(msg)

    @property
    def area_km2(self) -> float:
        """Approximate area in square kilometres.

        Uses spherical approximation:
        $A \\approx (\\Delta lon \\cdot \\cos(lat_{mid})) \\cdot \\Delta lat \\cdot 111.32^2$
        """
        import math

        lat_mid = (self.south + self.north) / 2
        dlon_deg = self.east - self.west
        dlat_deg = self.north - self.south
        km_per_deg_lon = 111.32 * abs(math.cos(math.radians(lat_mid)))
        km_per_deg_lat = 111.32
        return dlon_deg * km_per_deg_lon * dlat_deg * km_per_deg_lat

    def intersection(self, other: BBox) -> BBox | None:
        """Compute intersection with another bbox.

        Args:
            other: Bounding box to intersect.

        Returns:
            Intersection bbox, or None if disjoint.
        """
        west = max(self.west, other.west)
        south = max(self.south, other.south)
        east = min(self.east, other.east)
        north = min(self.north, other.north)
        if west >= east or south >= north:
            return None
        return BBox(west=west, south=south, east=east, north=north)

    def expand(self, factor: float) -> BBox:
        """Expand bbox by factor around centre.

        Args:
            factor: Multiplier for half-extents (1.0 = no change).

        Returns:
            Expanded bbox.
        """
        lon_mid = (self.west + self.east) / 2
        lat_mid = (self.south + self.north) / 2
        half_lon = (self.east - self.west) / 2 * factor
        half_lat = (self.north - self.south) / 2 * factor
        return BBox(
            west=lon_mid - half_lon,
            south=lat_mid - half_lat,
            east=lon_mid + half_lon,
            north=lat_mid + half_lat,
        )

    def to_tuple(self) -> tuple[float, float, float, float]:
        """Return (west, south, east, north) tuple."""
        return (self.west, self.south, self.east, self.north)
