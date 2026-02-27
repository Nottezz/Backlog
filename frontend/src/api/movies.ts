import api from './axios'
import type { UserRead } from './auth'

export interface MovieCreate {
  title: string
  description?: string | null
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
  id: number
  title: string
  description: string | null
  year: number | null
  rating: number | null
  watchLink: string | null
  kpId: number | null
  imdbId: number | null
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

  async getById(id: number, onlyMine = false): Promise<MovieRead> {
    const { data } = await api.get<MovieRead>(`/movies/${id}`, {
      params: { only_mine: onlyMine },
    })
    return data
  },

  async create(movie: MovieCreate): Promise<MovieRead> {
    const { data } = await api.post<MovieRead>('/movies/', movie)
    return data
  },

  async update(id: number, movie: MovieUpdate): Promise<MovieRead> {
    const { data } = await api.put<MovieRead>(`/movies/${id}`, movie)
    return data
  },

  async patch(id: number, movie: MovieUpdate): Promise<MovieRead> {
    const { data } = await api.patch<MovieRead>(`/movies/${id}`, movie)
    return data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/movies/${id}`)
  },
}
