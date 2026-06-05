import api from './axios'
import type { UserRead } from './auth'

export interface MovieCreate {
  title: string
  description?: string | null
  note?: string | null
  year?: number | null
  rating?: number | null
  watchLink?: string | null
  kpId?: number | null
  imdbId?: number | null
  published?: boolean
}

export interface MovieUpdate extends Partial<MovieCreate> {
  watched?: boolean | null
}

export interface MovieRead {
  slug: string
  title: string
  description: string | null
  note: string | null
  year: number | null
  rating: number | null
  watchLink: string | null
  kpId: number | null
  imdbId: number | null
  imdbRating: number | null
  metacriticScore: number | null
  published: boolean
  user: UserRead
  watched: boolean
  createdAt: string
}

export interface MovieList {
  movies: MovieRead[]
}

export const moviesApi = {
  async getList(onlyMine = false): Promise<MovieList> {
    const { data } = await api.get<MovieList>('/movies/', {
      params: { only_mine: onlyMine },
    })
    return data
  },

  async getBySlug(slug: string, onlyMine = false): Promise<MovieRead> {
  const { data } = await api.get<MovieRead>(`/movies/${slug}`, {
    params: { only_mine: onlyMine },
  })
  return data
},

  async getRandom(excludeSlugs: string[] = []): Promise<MovieRead> {
    const params = new URLSearchParams()
    excludeSlugs.forEach((slug) => params.append('exclude_slugs', slug))
    const { data } = await api.get<MovieRead>('/movies/random', { params })
    return data
  },

  async create(movie: MovieCreate): Promise<MovieRead> {
    const { data } = await api.post<MovieRead>('/movies/', movie)
    return data
  },

  async patch(slug: string, movie: MovieUpdate): Promise<MovieRead> {
    const { data } = await api.patch<MovieRead>(`/movies/${slug}`, movie)
    return data
  },

  async delete(slug: string): Promise<void> {
    await api.delete(`/movies/${slug}`)
  },
}
